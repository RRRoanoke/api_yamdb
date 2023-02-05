from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MyPaginator
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, mixins, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Title, Review, Comment, Categories, Genres, Titles

from .permissions import IsAdmin, IsAdminModeratorAuthorOrReadOnly
from .serializers import SignUpSerializer, TokenSeriliazer, UserSerializer, CommentSerializer, ReviewSerialize, CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleSafeSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAdmin,
    ]
    lookup_field = "username"
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ["get", "post", "delete", "patch"]

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        url_path="me",
        permission_classes=[
            permissions.IsAuthenticated,
        ],  # todo нужно ли
    )
    def get_current_user(self, request):
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username_exists = User.objects.filter(
        username=serializer._validated_data["username"]
    ).exists()
    email_exists = User.objects.filter(
        email=serializer._validated_data["email"]
    ).exists()
    if email_exists and not username_exists:
        return Response(
            {"detail": "email exist"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not email_exists and username_exists:
        return Response(
            {"detail": "username exist"}, status=status.HTTP_400_BAD_REQUEST
        )

    user, flag = User.objects.get_or_create(
        username=serializer.validated_data["username"],
        email=serializer.validated_data["email"],
    )
    confirmation_code = default_token_generator.make_token(user)
    user.email_user(
        subject="Код подтверждения",
        message=f"Ваш код - {confirmation_code}",
        from_email="admin@admin.ru",
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def token(request):
    serializer = TokenSeriliazer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User, username=serializer.validated_data["username"]
        )
        confirmation_code = serializer.validated_data["confirmation_code"]
        if default_token_generator.check_token(user, confirmation_code):
            access_token = AccessToken.for_user(user)
            data = {
                "username": request.data["username"],
                "token": str(access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly, )
    
  def perform_create(self, serializer):
      title_id = self.kwargs.get('title_id')
      title = get_object_or_404(Title, id=title_id)
      review_id = self.kwargs.get('review_id')
      review = get_object_or_404(Review, id=review_id, title=title)
      serializer.save(author=self.request.user, review=review)
      
  def get_queryset(self):
      title_id = self.kwargs.get('title_id')
      title = get_object_or_404(Title, id=title_id)
      review_id = self.kwargs.get('review_id')
      review = get_object_or_404(Review, id=review_id, title=title)
      return Comment.objects.filter(review=review)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()
   
  
class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)
    pagination_class = MyPaginator
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Categories, slug=kwargs['pk'])
        if request.user.is_anonymous or request.user.is_superuser: #поменять анонимуса на админа
            self.perform_destroy(category)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)
    pagination_class = MyPaginator
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)

    def destroy(self, request, *args, **kwargs):
        genre = get_object_or_404(Genres, slug=kwargs['pk'])
        if request.user.is_anonymous or request.user.is_superuser:
            self.perform_destroy(genre)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (IsAdmin,)
    pagination_class = MyPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug',
                        'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update', 'destroy'):
            return TitleSerializer
        return TitleSafeSerializer
