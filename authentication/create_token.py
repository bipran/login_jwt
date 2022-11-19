import jwt
import datetime
from rest_framework import exceptions
from loginAuthentication.settings import SECRET_KEY

class TokenGenerate:
    @staticmethod
    def get_access_token(user_id):
        return jwt.encode({
            "user_id":user_id,
            "exp":datetime.datetime.now()+datetime.timedelta(seconds=20),
            "iat":datetime.datetime.now()
        },SECRET_KEY+"a",algorithm="HS256")
    
    @staticmethod
    def decode_access_token(token):
        try:
            payload = jwt.decode(token,SECRET_KEY+"a",algorithms="HS256")
            return payload["user_id"]
        except:
            raise exceptions.AuthenticationFailed("unauthenticated")
    
    @staticmethod
    def decode_refresh_token(token):
        try:
            payload = jwt.decode(token,SECRET_KEY+"r",algorithms="HS256")
            return payload["user_id"]
        except:
            raise exceptions.AuthenticationFailed("unauthenticated")
    
    @staticmethod
    def get_refresh_token(user_id):
        return jwt.encode({
            "user_id":user_id,
            "exp":datetime.datetime.now()+datetime.timedelta(days=1),
            "iat":datetime.datetime.now()
        },SECRET_KEY+"r",algorithm="HS256")