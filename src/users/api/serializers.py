from rest_framework import serializers
from users.models import User


class AritcleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
