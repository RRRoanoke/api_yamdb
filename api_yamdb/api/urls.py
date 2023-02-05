from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, signup, token, ReviewViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')


authurls = [
    path("signup/", signup, name="signup"),
    path("token/", token, name="token"),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(authurls)),
]
