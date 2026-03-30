from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Friendships

User = get_user_model()


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
    """
    Receives username, email, first_name and last_name from front-end
    Sends user_id, username, email, first_name and last_name to front-end
    """
    
    class Meta:
        model = User
        fields = ("user_id", "username", "email", "first_name", "last_name")


class SendFriendRequestSerializer(serializers.Serializer):
    """
    Receives user_id from front-end
    """

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="receiver"
    )


class UpdateFriendshipSerializer(serializers.Serializer):
    """
    Receives friendship_id from front-end
    """

    friendship_id = serializers.PrimaryKeyRelatedField(
        queryset=Friendships.objects.all(), source="friendship"
    )


class FriendshipSerializer(serializers.ModelSerializer):
    """
    Sends friendship id, status and username of friend to front-end
    """
    # Adds an additional  field called username
    username = serializers.SerializerMethodField()

    class Meta:
        model = Friendships
        fields = ("id", "status", "username")

    def get_username(self, obj):
        """
        Figures out friend and returns their username
        """
        
        user = self.context["request"].user
        if obj.sender == user:
            friend = obj.receiver
        else:
            friend = obj.sender
        return friend.username
