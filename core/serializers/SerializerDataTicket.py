from ..models.DataTicket import DataTicket
from rest_framework import serializers


class SerializerDataTicket(serializers.ModelSerializer):
    class Meta:
        model: DataTicket
        fields = "__all__"
