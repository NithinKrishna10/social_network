from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


from ..models import CustomUser, FriendRequest
from ..serializers.friend_serializers import FriendRequestSerializer, UserSerializer
from ..serializers.request_serializers import SendFriendRequestSerializer, RespondFriendRequestSerializer
from ..utils import api_response

class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=SendFriendRequestSerializer,
    )
    def post(self, request):
        to_user_id = request.data.get('to_user_id')
        
        if not to_user_id:
            return api_response(success=False, message="Recipient user ID is required", status=400)
        try:
            to_user = CustomUser.objects.get(id=to_user_id)
        except CustomUser.DoesNotExist:
            return api_response(success=False, message="Recipient user not found", status=404)

        from_user = request.user

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return api_response(success=False, message="Friend request already sent", status=400)

        if FriendRequest.objects.filter(from_user=from_user, timestamp__gte=timezone.now() - timedelta(minutes=1)).count() >= 3:
            return api_response(success=False, message="Friend request limit exceeded", status=429)

        try:
            friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user, status='pending')
            return api_response(success=True, message="Friend request sent successfully", data=FriendRequestSerializer(friend_request).data, status=201)
        except Exception as e:
            return api_response(success=False, message=f"An error occurred: {str(e)}", status=500)
    

class RespondFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=RespondFriendRequestSerializer)
    def post(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return api_response(success=False, message="Friend request not found", status=404)

        status_ = request.data.get('status')
        
        if status_ not in ['accepted', 'rejected']:
            return api_response(success=False, message="Invalid status", status=400)

        try:
            friend_request.status = status_
            friend_request.save()
            return api_response(success=True, message=f"Friend request {status}", data=FriendRequestSerializer(friend_request).data)
        except Exception as e:
            return api_response(success=False, message=f"An error occurred: {str(e)}", status=500)


class ListFriendsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(
            sent_requests__to_user=self.request.user,
            sent_requests__status='accepted'
        )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return api_response(success=True, message="List of friends retrieved", data=serializer.data)
        except Exception as e:
            return api_response(success=False, message=f"An error occurred: {str(e)}", status=500)

class ListPendingRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user, status='pending')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return api_response(success=True, message="List of pending friend requests retrieved", data=serializer.data)
        except Exception as e:
            return api_response(success=False, message=f"An error occurred: {str(e)}", status=500)
