from api.base.base_views import BaseAuthenticationView, BaseView
from api.base.serializers import ExceptionResponseSerializer
from api.functions.function import gen_hash_password
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db.models import F, OuterRef, Value, CharField, Subquery, Count, Q
from models.user.models import User
from api.v1.user.serializers import CreateUserSerializer, UpdateAvatarUserSerializer, UpdateUserSerializer

class UserView(BaseView):   
    pass

class UserAuthenticationView(BaseAuthenticationView):   
    @extend_schema(
        operation_id='Get list user',
        summary='Get list user',
        tags=["A. user"],
        description='Get list user',
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
    def get_list_user(self, request):
        users = User.objects.all().values("id","username","full_name",
                                        "role", "email", "address", 
                                        "phone", "avatar_url" ,"password",
                                        "avatar_provider","c_provider",
                                        "refresh_token","access_token")

        result ={
            "data":list(users),
            "mess":"Get list user success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id='Get info user',
        summary='Get info user',
        tags=["A. user"],
        description='Get info user',
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
    def get_info(self, request, pk):
        user = User.objects.filter(pk=pk).values("id", "username","full_name", 
                                                "email", "address", "avatar_provider",
                                                "c_provider", "phone", "avatar_url","password").first()
        result ={
            "data":user,
            "mess":"Get info user success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
            operation_id='Create user',
            summary='Create user',
            tags=["A. user"],
            description='Create user',
            parameters=None,
            request =CreateUserSerializer,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username =None
        if "username" in serializer.validated_data:
            username = serializer.validated_data['username']
            username =username.lower()

        full_name =None
        if "full_name" in serializer.validated_data:
            full_name = serializer.validated_data['full_name']

        email =None
        if "email" in serializer.validated_data:
            email = serializer.validated_data['email']

        address =None
        if "address" in serializer.validated_data:
            address = serializer.validated_data['address']

        phone =None
        if "phone" in serializer.validated_data:
            phone = serializer.validated_data['phone']

        intro =None
        if "intro" in serializer.validated_data:
            intro = serializer.validated_data['intro']

        profile =None
        if "profile" in serializer.validated_data:
            profile = serializer.validated_data['profile']

        password =None
        if "password" in serializer.validated_data:
            password = serializer.validated_data['password']
            password = gen_hash_password(password)

        role =None
        if "role" in serializer.validated_data:
            role = serializer.validated_data['role']

        avatar_url =None
        if "avatar_url" in serializer.validated_data:
            avatar_url = serializer.validated_data['avatar_url']

        user = User.objects.create(username= username,full_name = full_name, email=email,
                                    address = address, phone =phone, intro= intro,
                                    profile = profile, password = password, role = role, avatar_url= avatar_url)

        result = { "mess": "Create user success!", 
                   "data":{"id":user.id}}
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
            operation_id='Update user',
            summary='Update user',
            tags=["A. user"],
            description='Update user',
            parameters=None,
            request = UpdateUserSerializer,
            responses={ 
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def update_user(self, request ,pk):
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(pk=pk).first()
        if not user:
            return Response({"mess": "user not found!"}, status=status.HTTP_400_BAD_REQUEST)

        if "full_name" in serializer.validated_data:
            full_name = serializer.validated_data['full_name']
            user.full_name = full_name

        if "email" in serializer.validated_data:
            email = serializer.validated_data['email']
            user.email = email

        if "address" in serializer.validated_data:
            address = serializer.validated_data['address']
            user.address = address

        if "phone" in serializer.validated_data:
            phone = serializer.validated_data['phone']
            user.phone = phone

        if "intro" in serializer.validated_data:
            intro = serializer.validated_data['intro']
            user.intro = intro

        if "profile" in serializer.validated_data:
            profile = serializer.validated_data['profile']
            user.profile = profile

        if "role" in serializer.validated_data:
            role = serializer.validated_data['role']
            user.role = role
        
        user.save()
        result = {"mess": "Update user success!","data":None}
        return Response(result, status=status.HTTP_200_OK)

      
    @extend_schema(
            operation_id='Delete user',
            summary='Delete user',
            tags=["A. user"],
            description='Delete user',
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
    def delete_user(self, request , pk):
        user = User.objects.filter(pk=pk).first()
        if not user:
            # return Response({"mess": "user not found!"}, status=status.HTTP_400_BAD_REQUEST)
            return self.http_exception( "user not found!", "user not found!", status.HTTP_400_BAD_REQUEST)

        user.delete()  

        result = {"mess": "Delete user success!","data":None}
        return Response(result, status=status.HTTP_200_OK)


    @extend_schema(
            operation_id='Update avatar user',
            summary='Update avatar user',
            tags=["A. user"],
            description='Update avatar user',
            parameters=None,
            request = UpdateAvatarUserSerializer,
            responses={ 
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def update_avatar_user(self, request ,pk):
        serializer = UpdateAvatarUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(pk=pk).first()
        if not user:
            return self.http_exception(description="ID User do not exist")

        if "avatar_url" in serializer.validated_data:
            avatar_url = serializer.validated_data['avatar_url']
            user.avatar_url = avatar_url

        user.save() 

        result = {"mess": "Update avatar user success!","data":None}
        return Response(result, status=status.HTTP_200_OK)