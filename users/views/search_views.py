from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from drf_yasg import openapi

from ..models import CustomUser
from ..serializers.friend_serializers import UserSerializer
from ..utils import api_response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class SearchUserView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Search users by email or name",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ]
    )
    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        if "@" in query:
            return self.queryset.filter(email__iexact=query)
        else:
            return self.queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(username__icontains=query)
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.paginate_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return api_response(
                success=False, message=f"An error occurred: {str(e)}", status=500
            )
