from django.urls import path

from ..controllers.Tickets import publicActionsTIckets

urlpatterns = [
    path("public/", publicActionsTIckets),
    # path("getAll/", privateTicketsGetWebhook),
]
