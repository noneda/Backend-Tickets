from django.urls import path

from ..controllers.SendBasic import getBasics
from ..controllers.SearchUser import getUserByEmail, suggestUsersByEmail

urlpatterns = [
    path("basics/", getBasics),
    path("user/", getUserByEmail),
    path("suggest/", suggestUsersByEmail),
]
