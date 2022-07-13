from api.base.base_views import BaseAuthenticationView
from api.base.serializers import ExceptionResponseSerializer
from api.functions.authentication import ClassStruct
from api.functions.function import check_match_password, gen_hash_password
from api.v1.common.serializers import FacebookSocialAuthSerializer, GoogleSocialAuthSerializer, LoginSerializer, RegisterSerializer, TokenSerializer
from config.contanst import USER_PROVIDER
from models.user.models import User
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db.models import F, OuterRef, Value, CharField, Subquery, Count, Q
from rest_framework_simplejwt.tokens import RefreshToken , Token
from src.settings import SIMPLE_JWT
import jwt


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CommonView(GenericViewSet):   
    @extend_schema(
        operation_id='Login',
        summary='Login',
        tags=["AA. Common"],
        description='Login',
        parameters=None,
        request= LoginSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = User.objects.filter(username = username).values("id","username","full_name", "email", "address", "avatar_url", "avatar_provider", "password").first()
        macth_password = False
        if user:
            macth_password = check_match_password(password, user["password"])
        if not user or not macth_password:
            return Response({"data":None, "mess":"wrong usename or password !", "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        user_obj = ClassStruct(**dict(user))
        token = get_tokens_for_user(user_obj)
        user["refresh_token"] = token["refresh"]
        user["access_token"] = token["access"]
        user["provider"] = USER_PROVIDER
        
        user_update = User.objects.filter(username = username).first()
        user_update.refresh_token = token["refresh"]
        user_update.access_token = token["access"]
        user_update.c_provider = USER_PROVIDER
        user_update.save()

        result ={
            "data":{
                "username":user["username"],
                "full_name":user["full_name"], 
                "email":user["email"], 
                "address":user["address"], 
                "avatar_url":user["avatar_url"],
                "avatar_provider":user["avatar_url"],
                "refresh_token":user["refresh_token"],
                "access_token":user["access_token"],
                "provider":user["provider"],
            },
            "status":status.HTTP_200_OK,
            "mess":"Login success!",
        }
        return Response(result, status=status.HTTP_200_OK)


    @extend_schema(
        operation_id='Register',
        summary='Register',
        tags=["AA. Common"],
        description='Register',
        parameters=None,
        request= RegisterSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        password = gen_hash_password(password)
        email = serializer.validated_data['email']
        full_name = serializer.validated_data['full_name']

        user = User.objects.create(username = username, email = email, full_name = full_name, password= password)

        result ={
            "data":{
                "username":user.username,
                "full_name":user.full_name, 
                "email":user.email, 
                "address":user.address, 
                "avatar_url":user.avatar_url
            },
            "status":status.HTTP_200_OK,
            "mess":"user register success!"
        }
        return Response(result, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='Log out',
        summary='Log out',
        tags=["AA. Common"],
        description='Log out',
        parameters=None,
        request= TokenSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def log_out(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        
        try:
            parse_token =jwt.decode(token,SIMPLE_JWT['SIGNING_KEY'],algorithms=[SIMPLE_JWT['ALGORITHM']])
            user = User.objects.filter(pk= parse_token["user_id"]).first()
            user.refresh_token = None
            user.access_token = None 
            user.c_provider = None 
            user.save()

        except:
            return Response({"mess":"Token invalid or expired!", "status": status.HTTP_400_BAD_REQUEST,"data":None}, status=status.HTTP_400_BAD_REQUEST)
    
        result ={
            "data":None,
            "status":status.HTTP_200_OK,
            "mess":"logout success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id='Check token',
        summary='Check token',
        tags=["AA. Common"],
        description='Check token',
        parameters=None,
        request= TokenSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def check_token(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        try:
            parse_token = jwt.decode(token,SIMPLE_JWT['SIGNING_KEY'],algorithms=[SIMPLE_JWT['ALGORITHM']])
        except:
            return Response({"mess":"Token invalid or expired!", "status": status.HTTP_400_BAD_REQUEST,"data":None}, status=status.HTTP_400_BAD_REQUEST)

        result ={
            "data":parse_token,
            "status":status.HTTP_200_OK,
            "mess":"parse token success!"
        }
        return Response(result, status=status.HTTP_200_OK)
    

    @extend_schema(
        operation_id='Personal profile',
        summary='Personal profile',
        tags=["AA. Common"],
        description='Personal profile',
        parameters=None,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def profile_info(self, request, pk):
        user = User.objects.filter(pk=pk).values("id", "username","full_name", "email", "address", "phone", "avatar_url").first()
        result ={
            "data":user,
            "status":status.HTTP_200_OK,
            "mess":"Get profile info success!"
        }
        return Response(result, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='Google Login',
        summary='Google Login',
        tags=["AA. Common"],
        description='Google Login',
        parameters=None,
        request= GoogleSocialAuthSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def google_login(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_user = serializer.validated_data['auth_token']

        email = auth_user['email']
        name = auth_user['name']
        provider = auth_user['provider']
        print("auth_user", auth_user)


        # user = User.objects.create(username = username, email = email, full_name = name, password= password)
        # token = get_tokens_for_user(user)

        result ={
            "data":{
                # "username":user.username,
                # "full_name":user.full_name, 
                # "email":user.email, 
                # "address":user.address, 
                # "avatar_url":user.avatar_url
            },
            "status":status.HTTP_200_OK,
            "token":"token"
        }
        return Response(result, status=status.HTTP_200_OK)
    
    @extend_schema(
        operation_id='Facebook Login',
        summary='Facebook Login',
        tags=["AA. Common"],
        description='Facebook Login',
        parameters=None,
        request= FacebookSocialAuthSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def facebook_login(self, request):
        serializer = FacebookSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_user = serializer.validated_data['auth_token']
        print("auth_user", auth_user)

        email = auth_user['email']
        name = auth_user['name']
        provider = auth_user['provider']


        # user = User.objects.create(username = username, email = email, full_name = name, password= password)
        # token = get_tokens_for_user(user)

        result ={
            "data":{
                # "username":user.username,
                # "full_name":user.full_name, 
                # "email":user.email, 
                # "address":user.address, 
                # "avatar_url":user.avatar_url
            },
            "status":status.HTTP_200_OK,
            "token":"token"
        }
        return Response(result, status=status.HTTP_200_OK)