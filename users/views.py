from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    FriendshipsSerializer,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Friendships

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

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
    Sends friend request to target user
    """

    def post(self, request):

        sender = request.user

        # Get the receiver's friend_id
        friend_id = request.data.get("friend_id")

        # Try to find user with friend_id
        try:
            receiver = User.objects.get(friend_id=friend_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Prevent user from friending themself
        if receiver == sender:
            return Response({"error": "You cannot friend yourself"}, status=400)

        # Check if receiver has already sent the user a friend request
        reverse_request = Friendships.objects.filter(
            sender=receiver, receiver=sender, status="pending"
        ).first()

        if reverse_request:
            # Update the friendship status to accepted
            reverse_request.status = "accepted"
            reverse_request.save()

            return Response({"message": "Friend added successfully"})

        # Create Friendships instance
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

        friendship = get_object_or_404(
            Friendships,
            id=request.data.get("friend_id"),
            receiver=request.user,
            status="pending",
        )

        # Update status to accepted
        friendship.status = "accepted"
        friendship.save()

        return Response({"message": "Friend added successfully"}, status=200)


class RejectFriendRequestView(APIView):
    """
    Rejects a friend request and deletes it from database
    """

    def post(self, request):

        friendship = get_object_or_404(
            Friendships,
            id=request.data.get("friend_id"),
            receiver=request.user,
            status="pending",
        )

        # Remove friendship from database
        friendship.delete()

        return Response({"message": "Friend request rejected"}, status=200)


class ListFriendsView(APIView):
    """
    Display a list of the user's current friends
    """

    def get(self, request):

        # Get a list of friendships
        friendships = Friendships.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)), status="accepted"
        )

        serializer = FriendshipsSerializer(
            friendships, many=True, context={"request": request}
        )

        return Response(serializer.data)
