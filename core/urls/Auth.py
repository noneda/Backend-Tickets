from django.urls import path

from ..auth.view import (
    doTokenWhenLoginUser,
    deleteTokenWhenLogOutUser,
    confirmationToken,
)

urlpatterns = [
    # * Post
    path("auth/", doTokenWhenLoginUser),
    path("logout/", deleteTokenWhenLogOutUser),
    path("confirm/", confirmationToken),
]
