from ..models.TypeTicket import TypeTicket
from rest_framework import serializers


class SerializerTypeTicket(serializers.ModelSerializer):
    class Meta:
        model: TypeTicket
        fields = "__all__"
