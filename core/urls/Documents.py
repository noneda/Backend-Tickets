from django.urls import path

from ..controllers.Documents import publicDocuments

urlpatterns = [
    path("send/", publicDocuments, name="ManegeDocuments"),
]
