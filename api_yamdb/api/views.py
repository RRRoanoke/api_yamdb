from rest_framework import filters, mixins, status, viewsets

from rest_framework.response import Response
from reviews.models import Categories, Genres, Titles
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleSafeSerializer)
from .pagination import MyPaginator
from .permissions import AdminOrReadonly


class ListCreateDeleteViewSet(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadonly,)
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
    permission_classes = (AdminOrReadonly,)
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
    permission_classes = (AdminOrReadonly,)
    pagination_class = MyPaginator
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug',
                        'genre__slug', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update', 'destroy'):
            return TitleSerializer
        return TitleSafeSerializer
