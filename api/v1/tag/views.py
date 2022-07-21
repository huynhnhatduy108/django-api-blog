from api.base.base_views import BaseAuthenticationView, BaseView
from api.base.serializers import ExceptionResponseSerializer
from api.functions.function import gen_random_string, gen_slug
from api.v1.tag.schemas import PARAMETER_SEARCH_TAG
from api.v1.tag.serializers import CreateTagSerializer, SearchTagSerializer, UpdateTagSerializer
from models.post.models import PostTag
from models.tag.models import Tag
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db.models import F, OuterRef, Value, CharField, Subquery, Count, Q

class TagView(BaseView):   
    @extend_schema(
        operation_id='Get list tag',
        summary='Get list tag',
        tags=["D. tag"],
        description='Get list tag',
        # parameters=PARAMETER_SEARCH_TAG,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def get_list_tag(self, request):
        tags = Tag.objects.all().annotate(tag_id =F('id'),
                                        post_count=Subquery(PostTag.objects.filter(
                                        tag_id=OuterRef('tag_id'))
                                        .values("tag_id")
                                        .annotate(count=Count('id'))
                                        .values('count'))).values("id","slug", "title", "meta_title","description","post_count").order_by("-id")

        result ={
            "data":list(tags),
            "mess":"Get list tag success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id='Search list tag',
        summary='Search list tag',
        tags=["D. tag"],
        description='Search list tag',
        parameters=PARAMETER_SEARCH_TAG,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def search_list_tag(self, request):
        serializer = SearchTagSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        tags = Tag.objects.all()
        keyword = None
        if "keyword" in serializer.validated_data:
            keyword = serializer.validated_data['keyword']
            if keyword:
                tags = tags.filter(Q(meta_title__icontains= keyword)| 
                                    Q(description__icontains= keyword)|Q(title__icontains= keyword))

        tags = tags.values("id","slug", "title", "meta_title","description").order_by("-id")

        self.paginate(tags)
        data = self.response_paging(self.paging_list)   
        
        result ={
            "data":data,
            "mess":"Get list tag success!"
        }
        return Response(result, status=status.HTTP_200_OK)

class TagAuthenticationView(BaseAuthenticationView): 
   
    @extend_schema(
        operation_id='Get info tag',
        summary='Get info tag',
        tags=["D. tag"],
        description='Get info tag',
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
        tag = Tag.objects.filter(pk=pk).values("id","slug", "title", "meta_title","description").first()
        result ={
            "data":tag,
            "mess":"Get info tag success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
            operation_id='Create tag',
            summary='Create tag',
            tags=["D. tag"],
            description='Create tag',
            parameters=None,
            request =CreateTagSerializer,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def create_tag(self, request):
        serializer = CreateTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = None
        slug = None
        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']
            slug = gen_slug(title)
            
        meta_title =None
        if "meta_title" in serializer.validated_data:
            meta_title = serializer.validated_data['meta_title']

        description =None
        if "description" in serializer.validated_data:
            description = serializer.validated_data['description']

        tag = Tag.objects.create(title= title, meta_title = meta_title, description = description, slug = slug)

        result = { "mess": "Create tag success!", 
                   "data":{"id":tag.id}}
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
            operation_id='Update tag',
            summary='Update tag',
            tags=["D. tag"],
            description='Update tag',
            parameters=None,
            request = UpdateTagSerializer,
            responses={ 
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def update_tag(self, request ,pk):
        serializer = UpdateTagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tag = Tag.objects.filter(pk=pk).first()
        if not tag:
            return Response({"mess": "tag not found!"}, status=status.HTTP_400_BAD_REQUEST)
    
        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']
            tag.title = title
            slug = gen_slug(title)
            tag.slug = slug
            
        if "meta_title" in serializer.validated_data:
            meta_title = serializer.validated_data['meta_title']
            tag.meta_title = meta_title

        if "description" in serializer.validated_data:
            description = serializer.validated_data['description']
            tag.description = description

        tag.save()

        result = { "mess": "Create tag success!", 
                   "data":{"id":tag.id}}
        
        return Response(result, status=status.HTTP_201_CREATED)

       
    @extend_schema(
            operation_id='Delete tag',
            summary='Delete tag',
            tags=["D. tag"],
            description='Delete tag',
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
    def delete_tag(self, request ,pk):
        tag = Tag.objects.filter(pk=pk).first()
        if not tag:
            return Response({"mess": "tag not found!"}, status=status.HTTP_400_BAD_REQUEST)
        tag.delete()  

        result = {"mess": "Delete tag success!","data":None}
        return Response(result, status=status.HTTP_200_OK)
