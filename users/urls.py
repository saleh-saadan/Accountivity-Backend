# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "friends/request/",
        views.SendFriendRequestView.as_view(),
        name="friend_request",
    ),
    path(
        "friends/add/",
        views.AcceptFriendRequestView.as_view(),
        name="friend_add",
    ),
    path(
        "friends/reject/",
        views.RejectFriendRequestView.as_view(),
        name="friend_reject",
    ),
    path(
        "friends/lists/",
        views.ListFriendsView.as_view(),
        name="friends_list",
    ),
    path(
        "friends/pending/",
        views.ListPendingRequestsView.as_view(),
        name="friends_pending",
    ),
    path(
        "me/",
         views.CurrentUserView.as_view(),
        name="current_user"
    ),
]
