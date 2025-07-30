from django.urls import path

from ..controllers.Helper import (
    helperUser,
    helperSendMailWhenCreate,
    helperSendMailWhenPatch,
)

urlpatterns = [
    path("user/", helperUser, name="GetOrCreateUser"),
    path("mail/", helperSendMailWhenCreate, name="SendMailWhenCreate"),
    path("privateMail/", helperSendMailWhenPatch, name="SendMailWhenCreate"),
]
