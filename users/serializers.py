from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Friendships


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Override simplejwt's default serializer to work with
    a custom string primary key (user_id) instead of integer id.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Embed user_id (our PK) into the token payload
        token["user_id"] = user.user_id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data


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
        fields = ("user_id", "username", "email", "first_name", "last_name")


class FriendshipsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Friendships
        fields = ["id", "status", "username"]

    def get_username(self, obj):
        user = self.context["request"].user
        if obj.sender == user:
            friend = obj.receiver
        else:
            friend = obj.sender
        return friend.username
