from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import UserActivities

from .views import (
    CreateUserView,
    LoginView,
    UpdatePasswordView,
    MeView,
    UsersView,
    UserActivitiesView,
)


router = DefaultRouter(trailing_slash=False)
router.register("create-user", CreateUserView, 'create user')
router.register("login", LoginView, 'login')
router.register("password-update", UpdatePasswordView, 'update password')
router.register("me", MeView, 'me')
router.register("activities", UserActivitiesView, 'activities log')
router.register("users", UsersView, 'users')

urlpatterns = [
    path("", include(router.urls)),
]

