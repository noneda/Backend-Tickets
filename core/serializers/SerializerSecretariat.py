from ..models.Secretariat import Secretariat
from rest_framework import serializers


class SerializerSecretariat(serializers.ModelSerializer):
    class Meta:
        model = Secretariat
        fields = "__all__"
