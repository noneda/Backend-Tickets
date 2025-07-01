from ..models.MyUser import MyUser
from rest_framework import serializers


class SerializerMyUser(serializers.ModelSerializer):
    class Meta:
        model: MyUser
        fields = "__all__"
