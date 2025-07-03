from django.urls import path, include
from ..controllers import info, verifyTokenSuccessful

"""Here have a path route /api && make a all Export from Rest Api"""
urlpatterns = [
    path("", info),
    path("test/", verifyTokenSuccessful),
    path("token/", include("core.urls.Auth")),
    path("get/", include("core.urls.GET")),
    path("ticket/", include("core.urls.Tickets")),
]
