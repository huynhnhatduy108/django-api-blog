from api.base.base_views import BaseAuthenticationView, BaseView
from api.base.serializers import ExceptionResponseSerializer
from api.functions.function import gen_slug
from api.v1.category.schemas import PARAMETER_SEARCH_CATEGORY
from api.v1.category.serializers import CreateCategorySerializer, SearchCategorySerializer, UpdateCategorySerializer
from models.category.models import Category
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.db.models import Q

class CategoryView(BaseView):   
    @extend_schema(
        operation_id='Get list category',
        summary='Get list category',
        tags=["E. category"],
        description='Get list category',
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
    def get_list_category(self, request):
        categorys = Category.objects.all().values("id","slug", "title", "meta_title","description", "thumbnail").order_by("-id")
        result ={
            "data":list(categorys),
            "mess":"Get list category success!"
        }
        return Response(result, status=status.HTTP_200_OK)
    
    @extend_schema(
            operation_id='Search list category',
            summary='Search list category',
            tags=["E. category"],
            description='Search list category',
            parameters=PARAMETER_SEARCH_CATEGORY,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def search_list_category(self, request):
        serializer = SearchCategorySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        categorys = Category.objects.all()

        keyword = None
        if "keyword" in serializer.validated_data:
            keyword = serializer.validated_data['keyword']

        if keyword:
            categorys = categorys.filter(Q(meta_title__icontains= keyword)| 
                                Q(description__icontains= keyword)|Q(title__icontains= keyword))

        categorys = categorys.values("id","slug", "title", "meta_title","description", "thumbnail").order_by("-id")
        
        self.paginate(categorys)
        data = self.response_paging(self.paging_list)   

        result ={
            "data":data,
            "mess":"Get list category success!"
        }
        return Response(result, status=status.HTTP_200_OK)

class CategoryAuthenticationView(BaseAuthenticationView):
    
    @extend_schema(
        operation_id='Get info category',
        summary='Get info category',
        tags=["E. category"],
        description='Get info category',
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
        category = Category.objects.filter(pk=pk).values("id","slug", "title", "meta_title","description", "thumbnail").first()
        result ={
            "data":category,
            "mess":"Get info category success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
            operation_id='Create category',
            summary='Create category',
            tags=["E. category"],
            description='Create category',
            parameters=None,
            request =CreateCategorySerializer,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def create_category(self, request):
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parent = None
        if "parent" in serializer.validated_data:
            parent = serializer.validated_data['parent']
            if parent:
                category_parent = Category.objects.filter(id = parent).first()
                if not category_parent:
                    return Response({"mess": "parent do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
                parent = category_parent
            else:
                parent = None

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

        thumbnail =None
        if "thumbnail" in serializer.validated_data:
            thumbnail = serializer.validated_data['thumbnail']

        category = Category.objects.create(parent = parent, title= title, meta_title = meta_title, description = description, thumbnail = thumbnail,slug = slug)

        result = { "mess": "Create category success!", 
                   "data":{"id":category.id}}
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
            operation_id='Update category',
            summary='Update category',
            tags=["E. category"],
            description='Update category',
            parameters=None,
            request = UpdateCategorySerializer,
            responses={ 
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def update_category(self, request ,pk):
        serializer = UpdateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = Category.objects.filter(pk=pk).first()
        if not category:
            return Response({"mess": "category do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if "parent" in serializer.validated_data:
            parent = serializer.validated_data['parent']
            if parent:
                category_parent = Category.objects.filter(id = parent).first()
                if not category_parent:
                    return Response({"mess": "parent do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
                category.parent = category_parent
            else:
                category.parent = None
    
        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']
            category.title = title
            slug = gen_slug(title)
            category.slug = slug
            
        if "meta_title" in serializer.validated_data:
            meta_title = serializer.validated_data['meta_title']
            category.meta_title = meta_title
      
        if "description" in serializer.validated_data:
            description = serializer.validated_data['description']
            category.description = description
     
        if "thumbnail" in serializer.validated_data:
            thumbnail = serializer.validated_data['thumbnail']
            category.thumbnail = thumbnail
        
        category.save()

        result = { "mess": "Create category success!", 
                   "data":{"id":category.id}}
        
        return Response(result, status=status.HTTP_201_CREATED)

       

    @extend_schema(
            operation_id='Delete category',
            summary='Delete category',
            tags=["E. category"],
            description='Delete category',
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
    def delete_category(self, request ,pk):
        category = Category.objects.filter(pk=pk).first()
        if not category:
            return Response({"mess": "category not found!"}, status=status.HTTP_400_BAD_REQUEST)
        category.delete()  

        result = {"mess": "Delete category success!","data":None}
        return Response(result, status=status.HTTP_200_OK)

