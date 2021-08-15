from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def username_is_not_me(value):
    if value == 'me':
        raise serializers.ValidationError(
            'You cannot use `me` as your username'
        )


def username_is_unique(value):
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError('This username already exists.')


class UserModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[username_is_unique]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[username_is_not_me, username_is_unique]
    )

    class Meta:
        model = User
        fields = ('email', 'username')


class CodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
