from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    SendFriendRequestSerializer,
    FriendshipSerializer,
    UpdateFriendshipSerializer,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Friendships

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user).data,
                "message": "User created successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class SendFriendRequestView(APIView):
    """
    Sends a friend request to target user
    """

    def post(self, request):
        sender = request.user

        serializer = SendFriendRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receiver = serializer.validated_data["receiver"]

        if receiver == sender:
            return Response({"error": "You cannot friend yourself"}, status=400)

        if Friendships.objects.filter(
            Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender), status="accepted"
        ).exists():
            return Response({"error": "You are already friends"}, status=400)

        # Check if receiver has already sent the user a friend request
        reverse_request = Friendships.objects.filter(
            sender=receiver, receiver=sender, status="pending"
        ).first()

        if reverse_request:
            reverse_request.status = "accepted"
            reverse_request.save()

            return Response({"message": "Friend added successfully"})

        friendship, created = Friendships.objects.get_or_create(
            sender=sender, receiver=receiver
        )
        if created:
            return Response({"message": "Request sent successfully!"})
        else:
            return Response({"message": "You have already sent a request to this user"})


class AcceptFriendRequestView(APIView):
    """
    Accepts friend request from a user
    """

    def post(self, request):
        serializer = UpdateFriendshipSerializer(data=request.data)
        serializer.is_valid()
        friendship = serializer.validated_data["friendship"]

        friendship.status = "accepted"
        friendship.save()

        return Response({"message": "Friend added successfully"}, status=200)


class RejectFriendRequestView(APIView):
    """
    Rejects a friend request and deletes it from the database
    """

    def post(self, request):
        serializer = UpdateFriendshipSerializer(data=request.data)
        serializer.is_valid()
        friendship = serializer.validated_data["friendship"]

        friendship.delete()

        return Response({"message": "Friend request rejected"}, status=200)


class ListFriendsView(APIView):
    """
    Displays a list of the user's current friends
    """

    def get(self, request):
        friendships = Friendships.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)), status="accepted"
        )

        serializer = FriendshipSerializer(
            friendships, many=True, context={"request": request}
        )

        return Response(serializer.data)


class ListReceivedPendingRequestsView(APIView):
    """
    Displays a list of the user's received pending requests
    """

    def get(self, request):
        friendships = Friendships.objects.filter(
            receiver=request.user,
            status="pending",
        )

        serializer = FriendshipSerializer(
            friendships, many=True, context={"request": request}
        )

        return Response(serializer.data)


class ListSentPendingRequestsView(APIView):
    """
    Displays a list of the user's sent pending requests
    """

    def get(self, request):
        friendships = Friendships.objects.filter(
            sender=request.user,
            status="pending",
        )
        serializer = FriendshipSerializer(
            friendships, many=True, context={"request": request}
        )
        return Response(serializer.data)


class RemoveFriendView(APIView):
    """
    Removes a friend and deletes the friendship from the datbase
    """

    def post(self, request):
        serializer = UpdateFriendshipSerializer(data=request.data)
        serializer.is_valid()
        friendship = serializer.validated_data["friendship"]

        friendship.delete()

        return Response({"message": "Friend removed"}, status=200)


class CurrentUserView(APIView):

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)