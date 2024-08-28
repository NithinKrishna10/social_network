from django.urls import path
from .views import SignupView, CustomAuthToken, UserSearchView, SendFriendRequestView, RespondFriendRequestView, FriendListView, PendingFriendRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('send-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('respond-request/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]
