from models.post.models import PostComment
from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    title = serializers.CharField(help_text="`title` of comment ",allow_null=True,required=False, allow_blank=True)
    parent = serializers.IntegerField(help_text="`parent` of comment ",required=False,allow_null=True,)
    content = serializers.CharField(help_text="`content` of comment ",allow_null=True,required=False, allow_blank=True)

    @staticmethod
    def validate(data):
        if "parent" in data:
            parent = data["parent"]
            if parent:
                comment_parent = PostComment.objects.filter(id= parent).first()
                if not comment_parent:
                    raise serializers.ValidationError("comment_parent do not exist!")

        if not "content" in data:
            raise serializers.ValidationError("content is required!")
        else:
            content = data["content"]
            if not content:
                raise serializers.ValidationError("content is required!")

        return data