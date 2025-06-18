from apps.account.models import User
from rest_framework import serializers

from apps.account.models import Profile


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'first_name',
            'last_name',
            'email',
            'password'
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'bio',
            'username',
            'avatar',
        )


class UserProfileRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )