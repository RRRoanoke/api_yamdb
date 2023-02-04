from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, signup, token

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")


authurls = [
    path("signup/", signup, name="signup"),
    path("token/", token, name="token"),
]

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/", include(authurls)),
]
