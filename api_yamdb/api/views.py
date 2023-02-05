from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from reviews.models import Title
from .serializers import (
    ReviewSerializer,
)

from .permission import (
    IsAdminModeratorAuthorOrReadOnly,
)
from django.shortcuts import get_object_or_404


class UserViewset(ModelViewSet):
    pass


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
