from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from django.contrib.auth import authenticate as authenticate_user
from rest_framework.response import Response

# def enforce_csrf(request):
#     check = CSRFCheck()
#     check.process_request(request)
#     reason = check.process_view(request, None, (), {})
#     if reason:
#         raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

class CustomAuthentication(JWTAuthentication):
    def get_tokens_for_user(self,user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        print(raw_token)
        # try:
        validate_token = self.get_validated_token(raw_token)
        # except BaseException as e:
            # user_cred = request.data
            # user = authenticate_user(
            #     username=user_cred.get('username',None), 
            #     password=user_cred.get('password',None))
            # return self.get_tokens_for_user(user)
        # enforce_csrf(request)
        return self.get_user(validate_token),validate_token