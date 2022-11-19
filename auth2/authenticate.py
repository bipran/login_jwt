from django.http import response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import InvalidToken
import requests


def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    check = CSRFCheck(request)
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)


class CustomAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get("access_token") or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken:
            data = requests.post(
                "http://127.0.0.1:8000/api/v1/token/refresh/", data={"refresh": request.COOKIES["refresh_token"]})
            if data.status_code == 200:
                res = data.json()
                validated_token = self.get_validated_token(res["access"])
            else:
                return
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token

    def get_validated_token(self, raw_token):
        return super().get_validated_token(raw_token)
