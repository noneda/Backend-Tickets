from django.urls import path

from ..auth.view import doTokenWhenLoginUser, deleteTokenWhenLogOutUser

urlpatterns = [
    # * Post
    path("auth/", doTokenWhenLoginUser),
    path("logout/", deleteTokenWhenLogOutUser),
]
