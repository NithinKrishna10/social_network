from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import CustomUser
from ..serializers.auth_serializers import SignupSerializer
from ..utils import api_response

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return api_response(success=False, message="Email and password are required", status=400)

        try:
            email = email.lower()
            validate_email(email)
        except ValidationError:
            return api_response(success=False, message="Invalid email format", status=400)

        if len(password) < 8:
            return api_response(success=False, message="Password must be at least 8 characters long", status=400)

        try:
            user = CustomUser.objects.create_user(email=email, username=email, password=password)
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return api_response(success=True, message="User signed up successfully", data=tokens, status=201)

        except IntegrityError:
            return api_response(success=False, message="User with this email already exists", status=400)

        except Exception as e:
            return api_response(success=False, message=f"An error occurred: {str(e)}", status=500)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return api_response(success=True, message="Login successful", data=tokens, status=200)
        return api_response(success=False, message="Invalid Credentials", status=400)
