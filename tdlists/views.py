from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import (
    TaskSerializer,
    UpdateTaskSerializer,
    TDListSerializer,
    UpdateTDListSerializer,
    MemberSerializer,
)
from .models import TDList, Task
from users.models import Friendships

User = get_user_model()


class CreateTDListView(APIView):
    """
    Creates a TDlist
    """

    def post(self, request):
        serializer = TDListSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "List created successfully"})


class ListTDListsView(APIView):
    """
    Displays the user's current TDLists
    """

    def get(self, request):
        td_lists = (
            TDList.objects.filter(Q(creator=request.user) | Q(members=request.user))
            .distinct()
            .prefetch_related("members", "tasks")
        )
        serializer = TDListSerializer(td_lists, many=True)

        return Response(serializer.data)


class UpdateTDListView(APIView):
    """
    Adds members, removes members and updates a TDList's name
    """

    def patch(self, request):
        serializer = UpdateTDListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        td_list = serializer.validated_data["list"]

        if request.user != td_list.creator:
            return Response({"detail": "Not allowed"}, status=403)

        if "name" in serializer.validated_data:
            td_list.name = serializer.validated_data["name"]
            td_list.save()

        if "add_members" in serializer.validated_data:
            td_list.members.add(*serializer.validated_data["add_members"])

        if "remove_members" in serializer.validated_data:
            td_list.members.remove(*serializer.validated_data["remove_members"])

        return Response({"message": "List updated successfully"})


class DeleteTDListView(APIView):
    """
    Deletes a TDList
    """

    def delete(self, request):
        serializer = UpdateTDListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        td_list = serializer.validated_data["list"]

        if request.user != td_list.creator:
            return Response({"detail": "Not allowed"}, status=403)

        td_list.delete()

        return Response({"message": "List deleted successfully"}, status=200)


class LeaveTDListView(APIView):
    """
    Removes user from the TDlist
    """

    def patch(self, request):
        serializer = UpdateTDListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        td_list = serializer.validated_data["list"]

        td_list.members.remove(request.user)

        return Response({"message": "Removed list successfully"}, status=200)


class ListPotentialMembersView(APIView):
    """
    Displays potential members that can be added to a TDList
    """

    def get(self, request, list_id):
        friendships = Friendships.objects.filter(
            (Q(sender=request.user) | Q(receiver=request.user)), status="accepted"
        ).select_related("sender", "receiver")
        friends = [
            (f.reciever if f.sender == request.user else f.sender) for f in friendships
        ]

        td_list = get_object_or_404(TDList, pk=list_id)
        members = set(td_list.members.all())

        potential_members = [pm for pm in friends if pm not in members]
        serializer = MemberSerializer(potential_members, many=True)

        return Response(serializer.data)


class CreateTaskView(APIView):
    """
    Creates a new task
    """

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Task created successfully"})


class UpdateTasksView(APIView):
    """
    Updates a Task's name and status
    """

    def patch(self, request):
        serializer = UpdateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.validated_data["task"]

        if request.user != task.creator:
            return Response({"detail": "Not allowed"}, status=403)

        if "name" in serializer.validated_data:
            task.name = serializer.validated_data["name"]

        if "completed" in serializer.validated_data:
            task.completed = serializer.validated_data["completed"]

        task.save()

        return Response({"message": "Task updated successfully"}, status=200)


class DeleteTaskView(APIView):
    """
    Deletes a Task
    """

    def delete(self, request):
        serializer = UpdateTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.validated_data["task"]

        if request.user != task.creator:
            return Response({"detail": "Not allowed"}, status=403)

        task.delete()

        return Response({"message": "Task deleted successfully"}, status=200)