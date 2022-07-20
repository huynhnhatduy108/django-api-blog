from unicodedata import category
from urllib import request
from wsgiref.util import request_uri
from api.base.base_views import BaseAuthenticationView, BaseView
from api.base.serializers import ExceptionResponseSerializer
from api.functions.function import compare_old_to_new_list, gen_slug_radom_string, get_value_list
from api.v1.post.schemas import PARAMETER_LIST_POST, PARAMETER_SEARCH_POST_BY_AUTHOR, PARAMETER_SEARCH_POST_BY_CATEGORY, PARAMETER_SEARCH_POST_BY_TAG
from api.v1.post.serializers import CreatePostSerializer, ListPostByAuthorSerializer, ListPostByCategorySerializer, ListPostByTagSerializer, ListPostSerializer, SearchPostByTitleSerializer, UpdatePostSerializer
from models.category.models import Category
from models.post.models import Post, PostCategory, PostMeta, PostTag
from models.tag.models import Tag
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.db.models import F, OuterRef, Value, CharField, Subquery, Count, Q

class PostAuthenticationView(BaseAuthenticationView):   
    @extend_schema(
            operation_id='List Post Search',
            summary='List Post Search',
            tags=["B. Post Search"],
            description='List Post Search',
            request = ListPostSerializer,
            # parameters= PARAMETER_SEARCH_POST,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def list(self, request):
        serializer = ListPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        posts = Post.objects.all()

        detail = 0
        if "detail" in serializer.validated_data:
            detail = serializer.validated_data['detail']

        if "tags" in serializer.validated_data:
            tags = serializer.validated_data['tags']
            # posts = Post.objects.filter(post_tags)

        if "categories" in serializer.validated_data:
            categories = serializer.validated_data['categories']
            # posts = Post.objects.filter()


        posts = Post.objects.all().annotate( post_id =F("id"), 
                                            parent_title =F("parent__title"), 
                                            author_name =F("author__full_name"),
                                            author_avatar =F("author__avatar_url"),
                                            ).values("post_id", "parent_id", 
                                                    "parent_title","slug", "title",
                                                    "meta_title","content", "summary",
                                                    "author_id", "author_name", "author_avatar",
                                                    "published_at").order_by("-post_id")

        self.paginate(posts)
        data = self.response_paging(self.paging_list)   

        if detail ==1:
            list_post = self.paging_list
            post_tags = PostTag.objects.filter(post__in = get_value_list(list_post, "post_id")).annotate(post_tag_id =F("id"),
                                                                        title =F("tag__title"),
                                                                        slug =F("tag__slug"),
                                                                        meta_title =F("tag__meta_title"),
                                                                        description =F("tag__description")
                                                                        ).values("post_tag_id", "tag_id","post_id", "slug", "meta_title", "description")

            post_categories = PostCategory.objects.filter(post__in=get_value_list(list_post, "post_id")).annotate(post_category_id =F("id"),
                                                                        title =F("category__title"),
                                                                        slug =F("category__slug"),
                                                                        meta_title =F("category__meta_title"),
                                                                        description =F("category__description")
                                                                        ).values("post_category_id", "post_id", "category_id", "slug", "meta_title", "description")
            
            for post in list_post:
                post["tags"] =[]
                post["categories"] =[]
                for post_tag in post_tags:
                    if post["post_id"] == post_tag["post_id"]:
                        post["tags"].append({
                                            "tag_id": post_tag["tag_id"],
                                            "post_tag_id":post_tag["post_tag_id"],
                                            "slug": post_tag["slug"],
                                            "meta_title": post_tag["meta_title"],
                                            "description": post_tag["description"],
                                             })
                for post_category in post_categories:
                    if post["post_id"] == post_category["post_id"]:
                        post["categories"].append({
                                            "category_id": post_category["category_id"],
                                            "post_category_id": post_category["post_category_id"],
                                            "slug": post_category["slug"],
                                            "meta_title": post_category["meta_title"],
                                            "description": post_category["description"],
                                             })     

            data = self.response_paging(list_post)   
        
        result ={
            "data":data,
            "mess":"Get list Post success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
            operation_id='Create Post',
            summary='Create Post',
            tags=["B. Post"],
            description='Create Post',
            parameters=None,
            request =CreatePostSerializer,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def create_post(self, request):
        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parent = None
        if "parent" in serializer.validated_data:
            parent = serializer.validated_data['parent']   

        title = None
        slug = None
        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']
            slug = gen_slug_radom_string(title, 8)

        meta_title = None
        if "meta_title" in serializer.validated_data:
            meta_title = serializer.validated_data['meta_title']

        content = None
        if "content" in serializer.validated_data:
            content = serializer.validated_data['content']

        summary = None
        if "summary" in serializer.validated_data:
            summary = serializer.validated_data['summary']


        published_at = None
        if "published_at" in serializer.validated_data:
            published_at = serializer.validated_data['published_at']

        thumbnail = None
        if "thumbnail" in serializer.validated_data:
            thumbnail = serializer.validated_data['thumbnail']

        post = Post.objects.create(parent= parent, title = title, slug =slug,
                                    content= content, summary = summary, meta_title= meta_title, 
                                    author_id = self.user["id"], published_at = published_at, thumbnail = thumbnail)
        
        tags = []
        if "tags" in serializer.validated_data:
            tags = serializer.validated_data['tags']
        if len(tags):
            PostTag.objects.bulk_create([PostTag(post_id=post.id, tag_id=tag_id) for tag_id in tags])

        categories = []
        if "categories" in serializer.validated_data:   
            categories = serializer.validated_data['categories']
        if len(categories):
            PostCategory.objects.bulk_create([PostCategory(post_id=post.id, category_id=category_id) for category_id in categories])
        

        result = { "mess": "Create Post success!", 
                   "data":{"id":post.id, "slug":post.slug}}
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
            operation_id='Update Post',
            summary='Update Post',
            tags=["B. Post"],
            description='Update Post',
            parameters=None,
            request = UpdatePostSerializer,
            responses={ 
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def update_post(self, request ,pk ,*args, **kwargs):
        serializer = UpdatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.check_permission_by_user_type(pk, kwargs.get("TYPE_API", None))

        post = Post.objects.filter(pk=pk).first()
        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)  

        if "parent" in serializer.validated_data:
            parent = serializer.validated_data['parent']   
            post.parent = parent

        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']
            if post.title != title:
                post.title = title
                slug = gen_slug_radom_string(title, 8)
                post.slug = slug

        if "meta_title" in serializer.validated_data:
            meta_title = serializer.validated_data['meta_title']
            post.meta_title = meta_title

        if "content" in serializer.validated_data:
            content = serializer.validated_data['content']
            post.content = content

        if "summary" in serializer.validated_data:
            summary = serializer.validated_data['summary']
            post.summary = summary

        if "published_at" in serializer.validated_data:
            published_at = serializer.validated_data['published_at']
            post.published_at = published_at
        
        if "thumbnail" in serializer.validated_data:
            thumbnail = serializer.validated_data['thumbnail']
            post.thumbnail = thumbnail
        
        if "tags" in serializer.validated_data:
            tags = serializer.validated_data['tags']
            post_tags = PostTag.objects.filter(post= pk).values("id", "tag_id")
            old_post_tags_id = get_value_list(post_tags,'tag_id')
            tags_add, tags_delete = compare_old_to_new_list(tags,old_post_tags_id)
            if len(tags_add):   
                PostTag.objects.bulk_create([PostTag(post_id=post.id, tag_id=tag_id) for tag_id in tags_add])
            if len(tags_delete):   
                PostTag.objects.filter(tag_id__in = tags_delete).delete()
        
        if "categories" in serializer.validated_data:
            categories = serializer.validated_data['categories']
            post_categories = PostCategory.objects.filter(post= pk).values("id", "category_id")
            old_post_categories_id = get_value_list(post_categories,'category_id')
            categories_add, categories_delete = compare_old_to_new_list(categories,old_post_categories_id)
            if len(categories_add):   
                PostCategory.objects.bulk_create([PostCategory(post_id=post.id, category_id=category_id) for category_id in categories_add])
            if len(categories_delete):   
                PostCategory.objects.filter(category_id__in = categories_delete).delete()

        post.save()

        result = {"mess": "Update Post success!", 
                   "data":{"id":post.id}}
        return Response(result, status=status.HTTP_201_CREATED) 
       

    @extend_schema(
            operation_id='Delete Post',
            summary='Delete Post',
            tags=["B. Post"],
            description='Delete Post',
            parameters=None,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )
    def delete_post(self, request , pk,*args, **kwargs):
        self.check_permission_by_user_type(pk, kwargs.get("TYPE_API", None))

        post = Post.objects.filter(pk=pk).first()

        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        
        post_meta = PostMeta.objects.filter(post_id=pk)
        post_tag = PostTag.objects.filter(post_id=pk)
        post_category = PostCategory.objects.filter(post_id=pk)
        post_meta.delete()
        post_tag.delete()
        post_category.delete()

        post.delete()  

        result = {"mess": "Delete Post success!","data":None}
        return Response(result, status=status.HTTP_200_OK)


class PostView(BaseView):   
    @extend_schema(
        operation_id='Get list Post',
        summary='Get list Post',
        tags=["B. Post"],
        description='Get list Post',
        parameters= PARAMETER_LIST_POST,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        request =None,
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def get_list_post(self, request, *args, **kwargs):
        serializer = ListPostSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        posts = Post.objects.all()

        detail = 0
        if "detail" in serializer.validated_data:
            detail = serializer.validated_data['detail']

        is_pagination = 1
        if "is_pagination" in serializer.validated_data:
            is_pagination = serializer.validated_data['is_pagination']
        
        keyword = None
        if "keyword" in serializer.validated_data:
            keyword = serializer.validated_data['keyword'] 
            posts = posts.filter(Q(title__icontains= keyword))
        
        tag = None
        if "tag" in serializer.validated_data:
            tag = serializer.validated_data['tag']
            if tag:
                posts = posts.filter(post_tag__tag_id =tag)

        category = None
        if "category" in serializer.validated_data:
            category = serializer.validated_data['category']  
            if category:
                posts = posts.filter(post_category__category_id=category)

        author = None
        if "author" in serializer.validated_data:
            author = serializer.validated_data['author']
            posts = posts.filter(author=author)

        posts = posts.annotate( post_id =F("id"), 
                                parent_title =F("parent__title"), 
                                author_name =F("author__full_name"),
                                author_avatar =F("author__avatar_url"),
                                ).values("post_id", "parent_id", 
                                        "parent_title","slug", "title",
                                        "meta_title","content", "summary",
                                        "author_id", "author_name", "author_avatar",
                                        "published_at", "thumbnail").order_by("-post_id")

        self.paginate(posts)
        data = self.response_paging(self.paging_list) if is_pagination ==1 else posts

        if detail ==1:
            list_post = self.paging_list if is_pagination == 1 else posts
            post_tags = PostTag.objects.filter(post__in = get_value_list(list_post, "post_id")).annotate(post_tag_id =F("id"),
                                                                        title =F("tag__title"),
                                                                        slug =F("tag__slug"),
                                                                        meta_title =F("tag__meta_title"),
                                                                        description =F("tag__description")
                                                                        ).values("post_tag_id", "tag_id","post_id", "title","slug", "meta_title", "description")

            post_categories = PostCategory.objects.filter(post__in=get_value_list(list_post, "post_id")).annotate(post_category_id =F("id"),
                                                                        title =F("category__title"),
                                                                        slug =F("category__slug"),
                                                                        meta_title =F("category__meta_title"),
                                                                        description =F("category__description"),
                                                                        thumbnail =F("category__thumbnail")
                                                                        ).values("post_category_id", "post_id","title", "category_id", "slug", "meta_title", "description", "thumbnail")
            
            for post in list_post:
                post["tags"] =[]
                post["categories"] =[]
                for post_tag in post_tags:
                    if post["post_id"] == post_tag["post_id"]:
                        post["tags"].append({
                                            "tag_id": post_tag["tag_id"],
                                            "post_tag_id":post_tag["post_tag_id"],
                                            "slug": post_tag["slug"],
                                            "title": post_tag["title"],
                                            "meta_title": post_tag["meta_title"],
                                            "description": post_tag["description"],
                                             })
                for post_category in post_categories:
                    if post["post_id"] == post_category["post_id"]:
                        post["categories"].append({
                                            "category_id": post_category["category_id"],
                                            "post_category_id": post_category["post_category_id"],
                                            "slug": post_category["slug"],
                                            "title": post_category["title"],
                                            "meta_title": post_category["meta_title"],
                                            "description": post_category["description"],
                                             })     

            data = self.response_paging(list_post) if is_pagination == 1 else list_post
        
        result ={
            "data":data,
            "mess":"Get list Post success!"
        }
        return Response(result, status=status.HTTP_200_OK)


    @extend_schema(
        operation_id='Get list Post by author',
        summary='Get list Post by author',
        tags=["B. Post"],
        description='Get list Post by author',
        parameters= PARAMETER_SEARCH_POST_BY_AUTHOR,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def get_list_post_by_author(self, request, author_id,*args, **kwargs):
        serializer = ListPostByAuthorSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        detail = 0
        if "detail" in request.query_params:
            detail = serializer.validated_data['detail']

        posts = Post.objects.filter(author_id = author_id).annotate( post_id =F("id"), 
                                                                    parent_title =F("parent__title"), 
                                                                    author_name =F("author__full_name"),
                                                                    author_avatar =F("author__avatar_url"),
                                                                    ).values("post_id", "parent_id", 
                                                                            "parent_title","slug", "title",
                                                                            "meta_title","content", "summary",
                                                                            "author_id", "author_name", "author_avatar",
                                                                            "published_at","thumbnail").order_by("-post_id")

        self.paginate(posts)
        data = self.response_paging(self.paging_list)  

        if detail ==1:
            list_post = self.paging_list
            post_tags = PostTag.objects.filter(post__in = get_value_list(list_post, "post_id")).annotate(post_tag_id =F("id"),
                                                                        title =F("tag__title"),
                                                                        slug =F("tag__slug"),
                                                                        meta_title =F("tag__meta_title"),
                                                                        description =F("tag__description")
                                                                        ).values("post_tag_id", "tag_id","post_id", "slug", "meta_title", "description")

            post_categories = PostCategory.objects.filter(post__in=get_value_list(list_post, "post_id")).annotate(post_category_id =F("id"),
                                                                        title =F("category__title"),
                                                                        slug =F("category__slug"),
                                                                        meta_title =F("category__meta_title"),
                                                                        description =F("category__description"),
                                                                        thumbnail =F("category__thumbnail")                                                                        
                                                                        ).values("post_category_id", "post_id", "category_id", "slug", "meta_title", "description","thumbnail")
            
            for post in list_post:
                post["tags"] =[]
                post["categories"] =[]
                for post_tag in post_tags:
                    if post["post_id"] == post_tag["post_id"]:
                        post["tags"].append({
                                            "tag_id": post_tag["tag_id"],
                                            "post_tag_id":post_tag["post_tag_id"],
                                            "slug": post_tag["slug"],
                                            "meta_title": post_tag["meta_title"],
                                            "description": post_tag["description"],
                                             })
                for post_category in post_categories:
                    if post["post_id"] == post_category["post_id"]:
                        post["categories"].append({
                                            "category_id": post_category["category_id"],
                                            "post_category_id": post_category["post_category_id"],
                                            "slug": post_category["slug"],
                                            "meta_title": post_category["meta_title"],
                                            "description": post_category["description"],
                                             })  

            data = self.response_paging(list_post)   

        result ={
            "data":data,
            "mess":"Get list Post by author success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id='Get list Post by Tag',
        summary='Get list Post by Tag',
        tags=["B. Post"],
        description='Get list Post by Tag',
        parameters = PARAMETER_SEARCH_POST_BY_TAG,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def get_list_post_by_tag(self, request, tag_id,*args, **kwargs):
        serializer = ListPostByTagSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        detail = 0
        if "detail" in request.query_params:
            detail = serializer.validated_data['detail']

        posts = PostTag.objects.filter(tag_id = tag_id).annotate(parent_id = F("post__parent_id"),
                                                                parent_title =F("post__parent__title"), 
                                                                slug = F("post__slug"), 
                                                                title = F("post__title"), 
                                                                meta_title = F("post__meta_title"), 
                                                                content = F("post__content"), 
                                                                summary = F("post__summary"), 
                                                                published_at = F("post__parent__title"),
                                                                author_id = F("post__author_id"),
                                                                author_name = F("post__author__full_name"),
                                                                author_avatar =F("post__author__avatar_url"),
                                                                ).values("post_id", "parent_id", 
                                                                        "parent_title","slug", "title",
                                                                        "meta_title","content", "summary",
                                                                        "author_id", "author_name", "author_avatar",
                                                                        "published_at","thumbnail").order_by("-post_id")

        self.paginate(posts)
        data = self.response_paging(self.paging_list)  

        if detail ==1:
            list_post = self.paging_list
            post_tags = PostTag.objects.filter(post__in = get_value_list(list_post, "post_id")).annotate(post_tag_id =F("id"),
                                                                        title =F("tag__title"),
                                                                        slug =F("tag__slug"),
                                                                        meta_title =F("tag__meta_title"),
                                                                        description =F("tag__description")
                                                                        ).values("post_tag_id", "tag_id","post_id", "slug", "meta_title", "description")

            post_categories = PostCategory.objects.filter(post__in=get_value_list(list_post, "post_id")).annotate(post_category_id =F("id"),
                                                                        title =F("category__title"),
                                                                        slug =F("category__slug"),
                                                                        meta_title =F("category__meta_title"),
                                                                        description =F("category__description"),
                                                                        thumbnail =F("category__thumbnail")                                                                                                                                               
                                                                        ).values("post_category_id", "post_id", "category_id", "slug", "meta_title", "description","thumbnail")

            for post in list_post:
                post["tags"] =[]
                post["categories"] =[]
                for post_tag in post_tags:
                    if post["post_id"] == post_tag["post_id"]:
                        post["tags"].append({
                                            "tag_id": post_tag["tag_id"],
                                            "post_tag_id":post_tag["post_tag_id"],
                                            "slug": post_tag["slug"],
                                            "meta_title": post_tag["meta_title"],
                                            "description": post_tag["description"],
                                             })
                for post_category in post_categories:
                    if post["post_id"] == post_category["post_id"]:
                        post["categories"].append({
                                            "category_id": post_category["category_id"],
                                            "post_category_id": post_category["post_category_id"],
                                            "slug": post_category["slug"],
                                            "meta_title": post_category["meta_title"],
                                            "description": post_category["description"],
                                             })  

            data = self.response_paging(list_post)   
                                                                    
        result ={
            "data":data,
            "mess":"Get list post by tag success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    
    @extend_schema(
        operation_id='Get list Post by Category',
        summary='Get list Post by Category',
        tags=["B. Post"],
        description='Get list Post by Category',
        parameters = PARAMETER_SEARCH_POST_BY_CATEGORY,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def get_list_post_by_category(self, request, category_id,*args, **kwargs):
        serializer = ListPostByCategorySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        detail = 0
        if "detail" in request.query_params:
            detail = serializer.validated_data['detail']

        posts = PostCategory.objects.filter(category_id = category_id).annotate(parent_id = F("post__parent_id"),
                                                                            parent_title =F("post__parent__title"), 
                                                                            slug = F("post__slug"), 
                                                                            title = F("post__title"), 
                                                                            meta_title = F("post__meta_title"), 
                                                                            content = F("post__content"), 
                                                                            summary = F("post__summary"), 
                                                                            thumbnail = F("post__thumbnail"), 
                                                                            published_at = F("post__parent__title"),
                                                                            author_id = F("post__author_id"),
                                                                            author_name = F("post__author__full_name"),
                                                                            author_avatar =F("post__author__avatar_url"),
                                                                            ).values("post_id", "parent_id", 
                                                                                    "parent_title","slug", "title",
                                                                                    "meta_title","content", "summary",
                                                                                    "author_id", "author_name", "author_avatar",
                                                                                    "published_at").order_by("-post_id")

        self.paginate(posts)
        data = self.response_paging(self.paging_list)   

        if detail ==1:
            list_post = self.paging_list
            post_tags = PostTag.objects.filter(post__in = get_value_list(list_post, "post_id")).annotate(post_tag_id =F("id"),
                                                                        title =F("tag__title"),
                                                                        slug =F("tag__slug"),
                                                                        meta_title =F("tag__meta_title"),
                                                                        description =F("tag__description")
                                                                        ).values("post_tag_id", "tag_id","post_id", "slug", "meta_title", "description")

            post_categories = PostCategory.objects.filter(post__in=get_value_list(list_post, "post_id")).annotate(post_category_id =F("id"),
                                                                        title =F("category__title"),
                                                                        slug =F("category__slug"),
                                                                        meta_title =F("category__meta_title"),
                                                                        description =F("category__description"),
                                                                        thumbnail =F("category__thumbnail")                                                                                                                                               
                                                                        ).values("post_category_id", "post_id", "category_id", "slug", "meta_title", "description", "thumbnail")

            for post in list_post:
                post["tags"] =[]
                post["categories"] =[]
                for post_tag in post_tags:
                    if post["post_id"] == post_tag["post_id"]:
                        post["tags"].append({
                                            "tag_id": post_tag["tag_id"],
                                            "post_tag_id":post_tag["post_tag_id"],
                                            "slug": post_tag["slug"],
                                            "meta_title": post_tag["meta_title"],
                                            "description": post_tag["description"],
                                             })
                for post_category in post_categories:
                    if post["post_id"] == post_category["post_id"]:
                        post["categories"].append({
                                            "category_id": post_category["category_id"],
                                            "post_category_id": post_category["post_category_id"],
                                            "slug": post_category["slug"],
                                            "meta_title": post_category["meta_title"],
                                            "description": post_category["description"],
                                             })  

            data = self.response_paging(list_post)   
       
        result ={
            "data":data,
            "mess":"Get list Post by Category success!"
        }
        return Response(result, status=status.HTTP_200_OK)


    @extend_schema(
        operation_id='Get info Post by id',
        summary='Get info Post by id',
        tags=["B. Post"],
        description='Get info Post by id',
        parameters=None,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def get_info_by_id(self, request, pk,*args, **kwargs):
        post = Post.objects.filter(pk=pk).annotate( post_id =F("id"), 
                                                    parent_title =F("parent__title"), 
                                                    author_name =F("author__full_name"),
                                                    author_avatar =F("author__avatar_url"),
                                                    ).values("post_id", "parent_id", 
                                                            "parent_title","slug", "title",
                                                            "meta_title","content", "summary",
                                                            "author_id", "author_name", "author_avatar",
                                                            "published_at",'thumbnail').first()
        
        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)  
    
        post_tags = PostTag.objects.filter(post = pk).annotate(post_tag_id =F("id"),
                                                                title =F("tag__title"),
                                                                slug =F("tag__slug"),
                                                                meta_title =F("tag__meta_title"),
                                                                description =F("tag__description")
                                                                ).values("post_tag_id", "tag_id", "slug", "meta_title", "description")

        post_categories = PostCategory.objects.filter(post = pk).annotate(post_category_id =F("id"),
                                                                        title =F("category__title"),
                                                                        slug =F("category__slug"),
                                                                        meta_title =F("category__meta_title"),
                                                                        description =F("category__description"),
                                                                        thumbnail =F("category__thumbnail")                                                                                                                                               
                                                                        ).values("post_category_id", "category_id", "slug", "meta_title", "description", "thumbnail")

        post["tags"] = list(post_tags)
        post["categories"] = list(post_categories)

        result ={
            "data":post,
            "mess":"Get info post success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
            operation_id='Get info Post by slug',
            summary='Get info Post by slug',
            tags=["B. Post"],
            description='Get info Post by slug',
            parameters=None,
            # request =CreatePostSerializer,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )

    def get_info_by_slug(self, request, slug,*args, **kwargs):
        post = Post.objects.filter(slug=slug).annotate( post_id =F("id"), 
                                                        parent_title =F("parent__title"), 
                                                        author_name =F("author__full_name"),
                                                        author_avatar =F("author__avatar_url"),
                                                        ).values("post_id", "parent_id", 
                                                                "parent_title","slug", "title",
                                                                "meta_title","content", "summary",
                                                                "author_id", "author_name", "author_avatar",
                                                                "published_at").first()
            
        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)  
            
        post_tags = PostTag.objects.filter(post= post["post_id"]).annotate(post_tag_id =F("id"),
                                                                            title =F("tag__title"),
                                                                            slug =F("tag__slug"),
                                                                            meta_title =F("tag__meta_title"),
                                                                            description =F("tag__description")
                                                                            ).values("post_tag_id", "tag_id", "slug", "meta_title", "description")

        post_categories = PostCategory.objects.filter(post= post["post_id"]).annotate(post_category_id =F("id"),
                                                                            title =F("category__title"),
                                                                            slug =F("category__slug"),
                                                                            meta_title =F("category__meta_title"),
                                                                            description =F("category__description"),
                                                                            thumbnail =F("category__thumbnail")                                                                                                                                               
                                                                            ).values("post_category_id", "category_id", "slug", "meta_title", "description","thumbnail")

        post["tags"] = list(post_tags)
        post["categories"] = list(post_categories)

        result ={
            "data":post,
            "mess":"Get info post success!"
        }
        return Response(result, status=status.HTTP_200_OK)
    

    @extend_schema(
            operation_id='Search post by title',
            summary='Search post by title',
            tags=["B. Post"],
            description='Search post by title',
            parameters=None,
            # request = CreatePostSerializer,
            responses={
                status.HTTP_200_OK: None,
                status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
                status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
            },
            examples=[
                # EXAMPLE_RESPONSE_TASK,
            ]
        )

    def search_post_by_keyword(self, request, keyword,*args, **kwargs):
        serializer =SearchPostByTitleSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        detail = 0
        if "detail" in request.query_params:
            detail = serializer.validated_data['detail']

        posts = Post.objects.filter(Q(title__icontains= keyword)| 
                                    Q(content__icontains= keyword)).annotate( post_id =F("id"), 
                                            parent_title =F("parent__title"), 
                                            author_name =F("author__full_name"),
                                            author_avatar =F("author__avatar_url"),
                                            ).values("post_id", "parent_id", 
                                                    "parent_title","slug", "title",
                                                    "meta_title","content", "summary",
                                                    "author_id", "author_name", "author_avatar",
                                                    "published_at").order_by("-post_id")

        self.paginate(posts)
        data = self.response_paging(self.paging_list)   

        if detail ==1:
            list_post = self.paging_list
            post_tags = PostTag.objects.filter(post__in = get_value_list(list_post, "post_id")).annotate(post_tag_id =F("id"),
                                                                        title =F("tag__title"),
                                                                        slug =F("tag__slug"),
                                                                        meta_title =F("tag__meta_title"),
                                                                        description =F("tag__description")
                                                                        ).values("post_tag_id", "tag_id","post_id", "slug", "meta_title", "description")

            post_categories = PostCategory.objects.filter(post__in=get_value_list(list_post, "post_id")).annotate(post_category_id =F("id"),
                                                                        title =F("category__title"),
                                                                        slug =F("category__slug"),
                                                                        meta_title =F("category__meta_title"),
                                                                        description =F("category__description"),
                                                                        thumbnail =F("category__thumbnail")                                                                                                                                               
                                                                        ).values("post_category_id", "post_id", "category_id", "slug", "meta_title", "description","thumbnail")

            for post in list_post:
                post["tags"] =[]
                post["categories"] =[]
                for post_tag in post_tags:
                    if post["post_id"] == post_tag["post_id"]:
                        post["tags"].append({
                                            "tag_id": post_tag["tag_id"],
                                            "post_tag_id":post_tag["post_tag_id"],
                                            "slug": post_tag["slug"],
                                            "meta_title": post_tag["meta_title"],
                                            "description": post_tag["description"],
                                             })
                for post_category in post_categories:
                    if post["post_id"] == post_category["post_id"]:
                        post["categories"].append({
                                            "category_id": post_category["category_id"],
                                            "post_category_id": post_category["post_category_id"],
                                            "slug": post_category["slug"],
                                            "meta_title": post_category["meta_title"],
                                            "description": post_category["description"],
                                             })  

            data = self.response_paging(list_post)   
       
        result ={
            "data":data,
            "mess":"Get list Post by Category success!"
        }
        return Response(result, status=status.HTTP_200_OK)

