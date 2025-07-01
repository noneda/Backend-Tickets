from ..models.Services import Services
from rest_framework import serializers


class SerializerServices(serializers.ModelSerializer):
    class Meta:
        model: Services
        fields = "__all__"
