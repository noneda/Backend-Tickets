from django.urls import path

from ..controllers.Tickets import publicActionsTickets, privateActionsTickets

urlpatterns = [
    path("public/", publicActionsTickets, name="ManagePublicTickets"),
    path("private/", privateActionsTickets, name="ManagePrivateTickets"),
]
