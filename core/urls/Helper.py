from django.urls import path

from ..controllers.Helper import helperUser, helperSendMail

urlpatterns = [
    path("user/", helperUser, name="GetOrCreateUser"),
    path("mail/", helperSendMail, name="SendMail"),
]
