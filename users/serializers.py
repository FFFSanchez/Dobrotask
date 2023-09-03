from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для юзеров"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'is_admin'
            # 'first_name',
            # 'last_name',
            # 'bio',
            # 'role',
        )
        extra_kwargs = {'password': {'write_only': True}}


# class MeSerializer(serializers.ModelSerializer):
#     """Сериализатор для своей учетной записи"""

#     class Meta:
#         model = User
#         fields = ('username', )  # 'email', 'first_name', 'last_name', 'bio')



# class UserSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     def get_is_subscribed(self, obj):
#         if (
#             'request' not in self.context or
#             self.context['request'].user.is_anonymous
#         ):
#             return False
#         return Follow.objects.filter(
#             author=obj, user=self.context['request'].user
#         ).exists()

#     def validate(self, data):
#         user = User(**data)
#         password = data.get('password')
#         try:
#             validators.validate_password(password=password, user=user)
#         except exceptions.ValidationError as e:
#             raise serializers.ValidationError(e.messages)
#         return super(UserSerializer, self).validate(data)

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'password',
#             'is_subscribed'
#         )
#         extra_kwargs = {'password': {'write_only': True}}