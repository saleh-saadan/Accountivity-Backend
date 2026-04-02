from django.urls import path
from . import views

urlpatterns = [
    path("lists/", views.ListTDListsView.as_view(), name="list-tdlists"),
    path("lists/create/", views.CreateTDListView.as_view(), name="create-tdlist"),
    path("lists/update/", views.UpdateTDListView.as_view(), name="update-tdlist"),
    path("lists/delete/", views.DeleteTDListView.as_view(), name="delete-tdlist"),
    path("lists/leave/", views.LeaveTDListView.as_view(), name="leave-tdlist"),
    path("lists/<int:list_id>/potential-members/", views.ListPotentialMembersView.as_view(), name="potential-members"),
    path("tasks/create/", views.CreateTaskView.as_view(), name="create-task"),
    path("tasks/update/", views.UpdateTasksView.as_view(), name="update-task"),
    path("tasks/delete/", views.DeleteTaskView.as_view(), name="delete-task"),
]