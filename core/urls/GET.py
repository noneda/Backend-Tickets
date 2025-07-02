from django.urls import path

from ..controllers.Secretariat import getSecretariat
from ..controllers.Services import getServices

urlpatterns = [path("services/", getServices), path("secretariat/", getSecretariat)]
