from django.urls import path
from .views.auth_views import SignupView, LoginView
from .views.search_views import SearchUserView
from .views.friend_views import SendFriendRequestView, RespondFriendRequestView, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchUserView.as_view(), name='search_users'),
    path('friend-request/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-request/respond/<int:pk>/', RespondFriendRequestView.as_view(), name='respond_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friend-requests/pending/', ListPendingRequestsView.as_view(), name='list_pending_requests'),
]
