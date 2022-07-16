from api.functions.function import is_email_valid
from config.contanst import ROLE_TYPE
from models.user.models import User
from rest_framework import serializers


class SearchUserSerializer(serializers.Serializer):
    keyword = serializers.CharField(help_text="Username, email of user",required=False,allow_null=True, allow_blank=True,)
    @staticmethod
    def validate(data):
        return data

class CreateUserSerializer(serializers.Serializer):
    username =  serializers.CharField(help_text="`username` of User ",allow_null=True,allow_blank=True,required=True)
    full_name =  serializers.CharField(help_text="`full_name` of User ",allow_null=True,allow_blank=True,required=False)
    email =  serializers.CharField(help_text="`email` of User ",allow_null=True,allow_blank=True,required=False)
    address =  serializers.CharField(help_text="`address` of User ",allow_null=True,allow_blank=True,required=False)
    phone = serializers.CharField(help_text="`phone` of User ",allow_null=True,allow_blank=True,required=False)
    intro = serializers.CharField(help_text="`intro` of User ",allow_null=True,allow_blank=True,required=False)
    profile =  serializers.CharField(help_text="`profile` of User ",allow_null=True,allow_blank=True,required=False)
    password = serializers.CharField(help_text="`password` of User ",allow_null=True,allow_blank=True,required=False)
    role =  serializers.IntegerField(help_text="`role` of User ",allow_null=True,required=False)
    avatar_url =  serializers.CharField(help_text="`avatar_url` of User ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
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

        if "role" in data:
            role = data["role"]
            if role not in ROLE_TYPE:
                raise serializers.ValidationError("role must in [0,1,2]!")
        return data

class UpdateUserSerializer(serializers.Serializer):
    full_name =  serializers.CharField(help_text="`full_name` of User ",allow_null=True,allow_blank=True,required=False)
    email =  serializers.CharField(help_text="`email` of User ",allow_null=True,allow_blank=True,required=False)
    address =  serializers.CharField(help_text="`address` of User ",allow_null=True,allow_blank=True,required=False)
    phone = serializers.CharField(help_text="`phone` of User ",allow_null=True,allow_blank=True,required=False)
    intro = serializers.CharField(help_text="`intro` of User ",allow_null=True,allow_blank=True,required=False)
    profile =  serializers.CharField(help_text="`profile` of User ",allow_null=True,allow_blank=True,required=False)
    role =  serializers.IntegerField(help_text="`role` of User ",allow_null=True,required=False)
    avatar_url =  serializers.CharField(help_text="`avatar_url` of User ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
        if "role" in data:
            role = data["role"]
            if role not in ROLE_TYPE:
                raise serializers.ValidationError("role must in [0,1,2]!")
        return data

class UpdateAvatarUserSerializer(serializers.Serializer):
    avatar_url =  serializers.CharField(help_text="`avatar_url` of User ",allow_null=True,allow_blank=True,required=True)

    @staticmethod
    def validate(data):
        avatar_url = data["avatar_url"]
        if not avatar_url:
            raise serializers.ValidationError("avatar_url must be string !")
        return data
