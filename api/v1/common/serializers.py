import os
from api.base.authentication import Google,Facebook
from api.functions.function import is_email_valid
from config.contanst import FACEBOOK_PROVIDER, GOOGLE_PROVIDER
from models.user.models import User
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="`username` of User systems",allow_null=True,allow_blank=True, required=False)
    password = serializers.CharField(help_text="`password`of User systems",allow_null=True,allow_blank=True, required=False)
   
    @staticmethod
    def validate(data):
        if not "username" in data or not "password" in data:
            raise serializers.ValidationError("username and password is required")
        return data 

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="`username` for User systems",allow_null=True,allow_blank=True, required=False)
    password = serializers.CharField(help_text="`password`for User systems",allow_null=True,allow_blank=True, required=False)
    email = serializers.CharField(help_text="`email` for User systems",allow_null=True,allow_blank=True, required=False)
    full_name = serializers.CharField(help_text="`full_name`for User systems",allow_null=True,allow_blank=True, required=False)
   
    @staticmethod
    def validate(data):
        if not "username" in data or not "password" in data:
            raise serializers.ValidationError("username and password is required")

        if not "email" in data:
            raise serializers.ValidationError("email is required")
        
        if "username" not in data or "email" not in data:
                raise serializers.ValidationError("username and email is required!")
        
        if "username" in data:
            username = data["username"]
            user = User.objects.filter(username = username).first()
            if user:
                raise serializers.ValidationError("username is existed!")
        
        if "email" in data:
            email = data["email"]
            if not is_email_valid(email):
                raise serializers.ValidationError("email is wrong format!")
            user = User.objects.filter(email = email).first()
            if user:
                raise serializers.ValidationError("email is existed!")
        
        if "password" not in data:
            raise serializers.ValidationError("password is required!")
        else:
            password = data["password"]
            if len(password)<8 or len(password)>20:
                raise serializers.ValidationError("password from 8 to 20 characters!")
        
        if not "full_name" in data:
            raise serializers.ValidationError("full_name is required")

        return data 


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="`token` of JWT",allow_null=True, allow_blank=True, required=False)
   
    @staticmethod
    def validate(data):
        if not "token" in data:
            raise serializers.ValidationError("token is required")
        return data 


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(help_text="`auth_token` of Facebook",)

    @staticmethod
    def validate(data):
        if "auth_token" not in data:
            raise serializers.ValidationError("token is required")
        else:
            auth_token= data["auth_token"]
            user_data = Facebook.validate(auth_token)
            try:
                user_data['provider'] = FACEBOOK_PROVIDER
                return user_data

            except Exception as identifier:
                raise serializers.ValidationError(
                    'The token  is invalid or expired. Please login again.'
                )

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(help_text="`auth_token` of Google",)

    @staticmethod
    def validate(data):
        if "auth_token" not in data:
            raise serializers.ValidationError("token is required")
        else:
            auth_token= data["auth_token"]
            user_data = Google.validate(auth_token)
            if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
                raise serializers.ValidationError('oops, who are you?')

            try:
                user_data['provider'] = GOOGLE_PROVIDER
                return user_data

            except Exception as identifier:
                raise serializers.ValidationError(
                    'The token  is invalid or expired. Please login again.'
                )




        
