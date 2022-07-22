from urllib import request
from django.shortcuts import render
from api.base.base_views import BaseAuthenticationView, BaseView
from api.base.serializers import ExceptionResponseSerializer
from api.functions.function import get_value_list
from api.v1.post_comment.schemas import PARAMETER_SEARCH_POST_BY_CATEGORY
from api.v1.post_comment.serializers import CommentSerializer
from models.post.models import Post, PostComment
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F, OuterRef, Value, CharField, Subquery, Count, Q
from drf_spectacular.utils import extend_schema

# Create your views here.
class CommentView(BaseView):
    @extend_schema(
        operation_id='Get list comment by post id',
        summary='Get list comment by post id',
        tags=["H. comment"],
        description='Get list comment by post id',
        # parameters=PARAMETER_SEARCH_POST_BY_CATEGORY,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def list_comment_by_post(self, request, post_id):
        post = Post.objects.filter(pk=post_id).first()
        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)  
        
        post_comments = PostComment.objects.filter(post_id = post_id, parent_id =None ).annotate(
                                                    user_name = F("author__full_name"),
                                                    user_avatar = F("author__avatar_url"),
                                                    comment_id=F("id"), 
                                                    comment_parent_id=F("parent_id")
                                                    ).values("comment_id",
                                                            "comment_parent_id",
                                                            "user_name",
                                                            "user_avatar",
                                                            "content",
                                                            "post_id",
                                                            "title", 
                                                            "created_at").order_by("-created_at")

        comments_reply = PostComment.objects.filter(parent__in =get_value_list(post_comments, 'comment_id') ).annotate(
                                                    user_name = F("author__full_name"),
                                                    user_avatar = F("author__avatar_url"),
                                                    comment_id=F("id"), 
                                                    comment_parent_id=F("parent_id")
                                                    ).values("comment_id",
                                                            "comment_parent_id",
                                                            "user_name",
                                                            "user_avatar",
                                                            "content",
                                                            "post_id",
                                                            "title", 
                                                            "created_at").order_by("created_at")

        list_comments = []
        for comment in post_comments:
            comment["sub_comment"] =[]
            for reply in comments_reply:
                if comment["comment_id"] == reply["comment_parent_id"]:
                   comment["sub_comment"].append(reply)
            list_comments.append(comment)

        result ={
            "data":list(list_comments),
            "mess":"Get list comment by post success!"
        }
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        operation_id='user comment to post',
        summary='user comment to post',
        tags=["H. comment"],
        description='user comment to post',
        parameters=None,
        request= CommentSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def user_comment_to_post(self, request ,post_id):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title= None
        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']

        parent= None
        if "parent" in serializer.validated_data:
            parent = serializer.validated_data['parent']

        content= None
        if "content" in serializer.validated_data:
            content = serializer.validated_data['content']

        post = Post.objects.filter(pk=post_id).first()
        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        comment = PostComment.objects.create(post_id = post_id, title = title, parent_id = parent, content = content)


        result ={
            "data":{
                "comment_id": comment.id,
                "title": comment.title,
                "comment_parent_id": comment.parent_id,
                "content": comment.content,
                "user_name":None,
                "user_avatar":None,
                "created_at": comment.created_at,
                "post_id": post_id,
                "sub_comment":[]
            },
            "mess":"create comment to post success!"
        }
        return Response(result, status=status.HTTP_200_OK)
    

class CommentAuthenticationView(BaseAuthenticationView):
    

    @extend_schema(
        operation_id='admin comment to post',
        summary='admin comment to post',
        tags=["H. comment"],
        description='admin comment to post',
        parameters=None,
        request= CommentSerializer,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def admin_comment_reply(self, request ,post_id):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title= None
        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']

        parent= None
        if "parent" in serializer.validated_data:
            parent = serializer.validated_data['parent']

        content= None
        if "content" in serializer.validated_data:
            content = serializer.validated_data['content']

        post = Post.objects.filter(pk=post_id).first()
        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        comment = PostComment.objects.create(post_id = post_id, title = title, parent_id = parent, content = content, author_id = self.user['id'])

        result ={
            "data":{
                "post_id": post_id,
                "comment_id": comment.id,
                "title": comment.title,
                "comment_parent_id": comment.parent_id,
                "content": comment.content,
                "user_name":comment.author.username,
                "user_avatar":comment.author.avatar_url,
                "created_at": comment.created_at,
                "sub_comment":[]

            },
            "mess":"create comment to post success!"
        }
        return Response(result, status=status.HTTP_200_OK)
    

    @extend_schema(
        operation_id='delete post comment',
        summary='delete post comment',
        tags=["H. comment"],
        description='delete post comment',
        parameters = None,
        request= None,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def delete_comment(self, request , comment_id):
        comments = PostComment.objects.filter(id = comment_id, parent_id = comment_id)
        if not comments:
            return Response({"mess": "comment do not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        comments.delete()

        result ={
            "data":None,
            "mess":"delete comment to post success!",
        }
        return Response(result, status=status.HTTP_200_OK)

    
    @extend_schema(
        operation_id='delete post comment by post id',
        summary='delete post comment by post id',
        tags=["H. comment"],
        description='delete post comment by post id',
        parameters = None,
        request= None,
        responses={
            status.HTTP_200_OK: None,
            status.HTTP_401_UNAUTHORIZED:ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[
            # EXAMPLE_RESPONSE_TASK,
        ]
    )
    def delete_comment_by_post_id(self, request , post_id):
        post  = Post.objects.filter(id= post_id).first()
        if not post:
            return Response({"mess": "post_id do not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        PostComment.objects.filter(post_id = post_id).delete()

        result ={
            "data":None,
            "mess":"delete comment of post success!",
        }
        return Response(result, status=status.HTTP_200_OK)
    
    

