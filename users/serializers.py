from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """ Users serializer """

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'is_admin'
        )
        extra_kwargs = {'password': {'write_only': True}}
