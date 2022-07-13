from urllib import request
from django.shortcuts import render
from api.base.base_views import BaseAuthenticationView, BaseView
from api.base.serializers import ExceptionResponseSerializer
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
        parameters=PARAMETER_SEARCH_POST_BY_CATEGORY,
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
        
        post_comments = PostComment.objects.filter(post_id = post_id).annotate(
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

        self.paginate(post_comments)
        data = self.response_paging(self.paging_list)   

        result ={
            "data":data,
            "mess":"Get list comment by post success!"
        }
        return Response(result, status=status.HTTP_200_OK)

class CommentAuthenticationView(BaseAuthenticationView):
    @extend_schema(
        operation_id='comment to post',
        summary='comment to post',
        tags=["H. comment"],
        description='comment to post',
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
    def comment_to_post(self, request ,post_id):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title= None
        if "title" in serializer.validated_data:
            title = serializer.validated_data['title']

        parent= None
        if "parent" in serializer.validated_data:
            parent = serializer.validated_data['parent']

        content= None
        if "title" in serializer.validated_data:
            content = serializer.validated_data['content']

        post = Post.objects.filter(pk=post_id).first()
        if not post:
            return Response({"mess": "post do not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        comment = PostComment.objects.create(post_id = post_id, title = title, parent_id = parent, content = content, author_id = self.user['id'])

        result ={
            "data":{
                "comment_id": comment.id,
                "comment_title": comment.title,
                "comment_parent_id": comment.parent_id,
                "comment_content": comment.content,
                "comment_author_id": comment.author_id,
                "comment_created_at": comment.created_at,
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
        comment = PostComment.objects.filter(pk=comment_id).first()
        if not comment:
            return Response({"mess": "comment do not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        comment.delete()

        result ={
            "data":None,
            "mess":"delete comment to post success!",
        }
        return Response(result, status=status.HTTP_200_OK)
    

