from api.base.serializers import ExceptionResponseSerializer
from api.v1.post_meta.serializers import CreatePostMetaSerializer, UpdatePostMetaSerializer
from models.post.models import Post, PostMeta
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db.models import F, OuterRef, Value, CharField, Subquery, Count, Q

class PostMetaView(GenericViewSet):   
    @extend_schema(
        operation_id='Get list postmeta',
        summary='Get list postmeta',
        tags=["F. postmeta"],
        description='Get list postmeta',
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
    def get_list_postmeta(self, request):
        postmetas = PostMeta.objects.all().values("id","content", "key")
        result ={
            "data":list(postmetas),
            "mess":"Get list postmeta success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id='Get info postmeta',
        summary='Get info postmeta',
        tags=["F. postmeta"],
        description='Get info postmeta',
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
        postmeta = PostMeta.objects.filter(pk=pk).values("id","content", "key").first()
        result ={
            "data":postmeta,
            "mess":"Get info postmeta success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
            operation_id='Create postmeta',
            summary='Create postmeta',
            tags=["F. postmeta"],
            description='Create postmeta',
            parameters=None,
            request =CreatePostMetaSerializer,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def create_postmeta(self, request):
        serializer = CreatePostMetaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = None
        if "post" in serializer.validated_data:
            post = serializer.validated_data['post']
            if post:
                post = Post.objects.filter(id = post).first()
                if not post:
                    return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
                post = post
            else:
                post = None

        content =None
        if "content" in serializer.validated_data:
            content = serializer.validated_data['content']

        key =None
        if "key" in serializer.validated_data:
            key = serializer.validated_data['key']

        postmeta = PostMeta.objects.create(post= post, content= content, key=key)

        result = { "mess": "Create postmeta success!", 
                   "data":{"id":postmeta.id}}
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
            operation_id='Update postmeta',
            summary='Update postmeta',
            tags=["F. postmeta"],
            description='Update postmeta',
            parameters=None,
            request = UpdatePostMetaSerializer,
            responses={ 
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def update_postmeta(self, request ,pk):
        serializer = UpdatePostMetaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        postmeta = PostMeta.objects.filter(pk=pk).first()
        if not postmeta:
            return Response({"mess": "postmeta do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if "post" in serializer.validated_data:
            post = serializer.validated_data['post']
            if post:
                post = postmeta.objects.filter(id = post).first()
                if not post:
                    return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
                postmeta.post = post
            else:
                postmeta.post = None

        if "content" in serializer.validated_data:
            content = serializer.validated_data['content']
            postmeta.content= content

        if "key" in serializer.validated_data:
            key = serializer.validated_data['key']
            postmeta.key= key

        postmeta.save()

        result = { "mess": "Create postmeta success!", 
                   "data":{"id":postmeta.id}}
        
        return Response(result, status=status.HTTP_201_CREATED)
 

    @extend_schema(
            operation_id='Delete postmeta',
            summary='Delete postmeta',
            tags=["F. postmeta"],
            description='Delete postmeta',
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
    def delete_postmeta(self, request ,pk):
        postmeta = PostMeta.objects.filter(pk=pk).first()
        if not postmeta:
            return Response({"mess": "postmeta not found!"}, status=status.HTTP_400_BAD_REQUEST)
        postmeta.delete()  

        result = {"mess": "Delete postmeta success!","data":None}
        return Response(result, status=status.HTTP_200_OK)
