from models.user.models import User
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from src.settings import SIMPLE_JWT
import jwt
import facebook
from google.auth.transport import requests
from google.oauth2 import id_token

class TokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    lang = None

    def authenticate(self, request):
        # try:
            auth = get_authorization_header(request).split()
            if not len(auth):
                raise exceptions.AuthenticationFailed({
                'error_code': "TOKEN_NOT_VALID",
                'description': "TOKEN_NOT_VALID"
            })
            receive_token = auth[1].decode('utf-8')
            parse_token = self.parse_token(receive_token)
            if not parse_token:
                raise exceptions.AuthenticationFailed({
                    'error_code': "INVALID_TOKEN_OR_EXPIRE",
                    'description': "INVALID_TOKEN_OR_EXPIRE"
                })

            user, err = self.check_user_and_token(parse_token, receive_token)
            if err:
                raise exceptions.AuthenticationFailed({
                    'error_code': err,
                    'description': err,
                })

            setattr(request, 'user', user)
            return user, None


    @staticmethod
    def parse_token(receive_token):
        try:
            parse_token =jwt.decode(receive_token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
        except:
            return None
        return parse_token

    @staticmethod
    def check_user_and_token(objects_token, receive_token):
        try:
            user = User.objects.filter(id=objects_token["user_id"]).first()
            if not user or user.access_token != receive_token:
                return None, "INVALID_TOKEN_OR_EXPIRE"
        except Exception:
            return None, "INVALID_TOKEN_OR_EXPIRE"
        return user, None


class TokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'api.base.authentication.TokenAuthentication'
    name = 'TokenAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer"
        }


class Facebook:
    @staticmethod
    def validate(auth_token):
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=name,email')
            return profile
        except:
            raise exceptions.AuthenticationFailed({
                    'error_code': "INVALID_TOKEN",
                    'description': "INVALID_TOKEN"
                })


class Google:
    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            raise exceptions.AuthenticationFailed({
                    'error_code': "INVALID_TOKEN",
                    'description': "INVALID_TOKEN"
                })