from django.urls import path

from ..controllers.Documents import publicSendDocuments

urlpatterns = [
    path("send/", publicSendDocuments, name="ManegeDocuments"),
]
