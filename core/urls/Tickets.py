from django.urls import path

from ..controllers.Tickets import publicActionsTickets

urlpatterns = [
    path("public/", publicActionsTickets, name="ManageTickets"),
]
