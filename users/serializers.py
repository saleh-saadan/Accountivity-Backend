# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Friendships


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "friend_id")


class FriendshipsSerializer(serializers.ModelSerializer):

    friend_info = serializers.SerializerMethodField()

    class Meta:
        model = Friendships
        fields = ["id", "status", "friend_info"]

    def get_friend_info(self, obj):

        user = self.context["request"].user

        # Figure out which one is the user viewing the friends list
        if obj.sender == user:
            friend = obj.receiver
        else:
            friend = obj.sender

        # Return dictionary of friend's data
        return {"username": friend.username}
