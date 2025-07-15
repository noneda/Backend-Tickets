from django.urls import path

from ..controllers.Tickets import publicActionsTIckets, privateTicketsGetWebhook

urlpatterns = [
    path("public/", publicActionsTIckets),
    path("getAll/", privateTicketsGetWebhook),
]
