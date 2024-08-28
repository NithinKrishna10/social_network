from datetime import timedelta  # Standard library import

from django.db.models import Q  # Django import

from rest_framework import generics, status  # Third-party imports
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Friendship  # Local application imports
from .serializers import UserSerializer, FriendshipSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class UserSearchView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('search', '')
        return User.objects.filter(Q(email__iexact=keyword) | Q(username__icontains=keyword))[:10]



class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        to_user = User.objects.get(id=to_user_id)
        from_user = request.user

        if Friendship.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'detail': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        if Friendship.objects.filter(from_user=from_user, created_at__gte=timezone.now() - timedelta(minutes=1)).count() >= 3:
            return Response({'detail': 'Friend request limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        Friendship.objects.create(from_user=from_user, to_user=to_user, status='pending')
        return Response({'detail': 'Friend request sent'}, status=status.HTTP_201_CREATED)

class RespondFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        friendship_id = request.data.get('friendship_id')
        action = request.data.get('action')
        friendship = Friendship.objects.get(id=friendship_id)

        if action == 'accept':
            friendship.status = 'accepted'
        elif action == 'reject':
            friendship.status = 'rejected'
        else:
            return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

        friendship.save()
        return Response({'detail': f'Friend request {action}ed'}, status=status.HTTP_200_OK)

class FriendListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()

class PendingFriendRequestsView(ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.received_requests.filter(status='pending')
