from asyncio.proactor_events import constants
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serrializer = UserSerializer(data=request.data)
        if serrializer.is_valid():
            serrializer.save()
            return Response({"msg": "Registration success"}, status=status.HTTP_200_OK)
        return Response({"error": serrializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class loginView(APIView):
    def post(self, request, format=None):
        # serializer = LoginSerializer(data=request.data)
        # if serializer.is_valid():
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token_for_user = get_tokens_for_user(user)
            csrf.get_token(request)
            response = Response(
                {"msg": "Login success", "data": token_for_user}, status=status.HTTP_200_OK)
            response.set_cookie(
                key="refresh_token",
                value=token_for_user["refresh"],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            response.set_cookie(
                key="access_token",
                value=token_for_user["access"],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            return response
        return Response({"error": "username or password is not valid"}, status=status.HTTP_400_BAD_REQUEST)


class DetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        user = User.objects.all()
        ser = LoginSerializer(user, many=True)
        return Response({"data": ser.data}, status=status.HTTP_200_OK)
