from ..models.Documents import Documents
from rest_framework import serializers


class SerializerDocuments(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"
