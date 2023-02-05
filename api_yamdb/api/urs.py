from rest_framework.routers import SimpleRouter
from .views import (
    CommentViewSet
)

router = SimpleRouter
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
