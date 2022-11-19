from os import access
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings
from django.middleware import csrf
from .authenticate import CustomAuthentication
from rest_framework.permissions import IsAuthenticated

from authentication.create_token import TokenGenerate


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterUser(APIView):
    pass

class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]
    def get(self,request,format=None,*args,**kwargs):
        return Response({"msg":"I am home view...."})

class TokenRefreshView(APIView):
    def post(self,request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = TokenGenerate.decode_refresh_token(refresh_token)
        access_token = TokenGenerate.get_access_token(id)
        response = Response()
        # response.set_cookie(
        #             key = settings.SIMPLE_JWT['AUTH_COOKIE'],
        #             value = access_token,
        #             expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        #             secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        #             httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        #             samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        #         )
        response.set_cookie("access_token",access_token,settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        return Response({"access":access_token},status=status.HTTP_200_OK)
class LoginView(APIView):
    def post(self,request,format=None,*args,**kwargs):
        print("I am here....")
        login_credential = request.data 
        response = Response()
        username = login_credential.get('username', None)
        password = login_credential.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # data = get_tokens_for_user(user)
                refresh = TokenGenerate.get_refresh_token(user.id)
                access = TokenGenerate.get_access_token(user.id)
                # response.set_cookie(
                #     key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                #     value = access,
                #     expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                #     secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                #     httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                #     samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                # )
                response.set_cookie(
                    key = 'refresh_token',
                    value = refresh,
                    expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully","access":access}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)