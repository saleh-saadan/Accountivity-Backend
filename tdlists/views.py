from .models import TDList, Task
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()


class CreateTDListView(APIView):
    """
    Creates a TDlist
    """

    def post(self, request):

        pass


class ListTDLIstsView(APIView):
    """
    Displays the user's current TDLists
    """

    def get(self, request):

        pass


class ListMembersView(APIView):
    """
    Displays members of a TDList
    """

    def get(self, request):

        pass


class ListPotentialMembersView(APIView):
    """
    Displays potential members that can be added to a TDList
    """

    def get(self, request):

        pass


class AddMembersView(APIView):
    """
    Adds more members to a TDList
    """

    def post(self, request):

        pass


class RemoveMembersView(APIView):
    """
    Removes members from a TDList
    """

    def delete(self, request):

        pass


class UpdateTDListView(APIView):
    """
    Updates a TDLists' name
    """

    def post(self, request):

        pass


class LeaveTDListView(APIView):
    """
    Removes user from a TDlist
    """

    def delete(self, request):

        pass


class DeleteTDListView(APIView):
    """
    Deletes a TDList
    """

    def delete(self, request):

        pass


class CreateTaskView(APIView):
    """
    Creates a new task
    """

    def post(self, request):

        pass


class ListTasksView(APIView):
    """
    Displays all the tasks in a TDList
    """

    def get(self, request):

        pass


class UpdateTasksView(APIView):
    """
    Updates a Tasks's name, status or due date
    """

    def post(self, request):

        pass
    

class DeleteTDListView(APIView):
    """
    Deletes a Task created by the user
    """

    def delete(self, request):

        pass