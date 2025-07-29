from django.urls import path

from ..controllers.SendBasic import getBasics
from ..controllers.SearchUser import getUserByEmail, suggestUsersByEmail

urlpatterns = [
    path("basics/", getBasics, name="getBasic"),
    path("user/", getUserByEmail, name="getUserByEmail"),
    path("suggest/", suggestUsersByEmail, name="suggestUserByEmail"),
]
