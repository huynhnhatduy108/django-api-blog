from tkinter.messagebox import NO
from models.category.models import Category
from models.post.models import Post
from models.tag.models import Tag
from models.user.models import User
from rest_framework import serializers
from datetime import datetime

class ListPostSerializer(serializers.Serializer):
    detail = serializers.IntegerField(help_text="Detail tags and categories of post",required=False,allow_null=True)

    @staticmethod
    def validate(data):
        error = []
        if "detail" in data:
            detail = data["detail"]
            if detail not in [0,1]:
                raise serializers.ValidationError("detail must be in [0,1]!")
        return data

class ListPostByAuthorSerializer(serializers.Serializer):
    title = serializers.CharField(help_text="Detail tags and categories of post",required=False,allow_null=True)

    @staticmethod
    def validate(data):
        error = []
        if "detail" in data:
            detail = data["detail"]
            if detail not in [0,1]:
                raise serializers.ValidationError("detail must be in [0,1]!")
        return data

class ListPostByTagSerializer(serializers.Serializer):
    detail = serializers.IntegerField(help_text="Detail tags and categories of post",required=False,allow_null=True)

    @staticmethod
    def validate(data):
        error = []
        if "detail" in data:
            detail = data["detail"]
            if detail not in [0,1]:
                raise serializers.ValidationError("detail must be in [0,1]!")
        return data

class ListPostByCategorySerializer(serializers.Serializer):
    detail = serializers.IntegerField(help_text="Detail tags and categories of post",required=False,allow_null=True)

    @staticmethod
    def validate(data):
        error = []
        if "detail" in data:
            detail = data["detail"]
            if detail not in [0,1]:
                raise serializers.ValidationError("detail must be in [0,1]!")
        return data

class SearchPostByTitleSerializer(serializers.Serializer):
    detail = serializers.IntegerField(help_text="Detail tags and categories of post",required=False,allow_null=True)

    @staticmethod
    def validate(data):
        error = []
        if "detail" in data:
            detail = data["detail"]
            if detail not in [0,1]:
                raise serializers.ValidationError("detail must be in [0,1]!")
        return data

class CreatePostSerializer(serializers.Serializer):
    parent = serializers.IntegerField(help_text="`parent` of Post ",required=False,allow_null=True,)
    title = serializers.CharField(help_text="`title` of Post ",allow_null=True,required=False, allow_blank=True)
    meta_title = serializers.CharField(help_text="`meta_title` of Post ",allow_null=True,required=False, allow_blank=True)
    content = serializers.CharField(help_text="`content` of Post ",allow_null=True,required=False, allow_blank=True)
    summary = serializers.CharField(help_text="`summary` of Post ",allow_null=True,required=False, allow_blank=True)
    published_at = serializers.CharField(help_text="`published_at` of Post ",allow_null=True,required=False, allow_blank=True)
    tags = serializers.ListField(child=serializers.IntegerField(help_text="list tags of Post"), allow_null=True,required=False)
    categories = serializers.ListField(child=serializers.IntegerField(help_text="list category of Post"), allow_null=True,required=False)
    thumbnail = serializers.CharField(help_text="`thumbnail` of Post ",allow_null=True,required=False, allow_blank=True)

    @staticmethod
    def validate(data):
        error = []

        if "parent" in data:
            parent = data["parent"]
            if parent is not None:
                parent = Post.objects.filter(id = parent).first()
                if not parent:
                    raise serializers.ValidationError("parent do not exist!")

        if "published_at" in data:
            published_at = data["published_at"]
            try:
                published_at = '{} 00:00:00'.format(published_at, '%d/%m/%Y %H:%M:%S')
                published_at = datetime.strptime(published_at, '%d/%m/%Y %H:%M:%S')
            except:
                raise serializers.ValidationError("published_at type is date %d/%m/%Y")
            data["published_at"] = published_at
        
        if "tags" in data:
            tags = data["tags"]
            if not isinstance(tags, list):
                raise serializers.ValidationError("tags must be array []!")
            if len(tags):
                list_tag = Tag.objects.filter(id__in = tags)
                if len(list_tag) != len(tags):
                    raise serializers.ValidationError("some tag is not exist or duplicate!")

        if "categories" in data:
            categories = data["categories"]
            if not isinstance(categories, list):
                raise serializers.ValidationError("categories must be array []!")
            if len(categories):
                list_category = Category.objects.filter(id__in = categories)
                if len(list_category) != len(categories):
                    raise serializers.ValidationError("some category is not exist or duplicate!")
        
        return data

class UpdatePostSerializer(serializers.Serializer):
    parent = serializers.IntegerField(help_text="`parent` of Post ",required=False, allow_null=True)
    title = serializers.CharField(help_text="`title` of Post ",allow_null=True,required=False, allow_blank=True)
    meta_title = serializers.CharField(help_text="`meta_title` of Post ",allow_null=True,required=False, allow_blank=True)
    content = serializers.CharField(help_text="`content` of Post ",allow_null=True,required=False)
    summary = serializers.CharField(help_text="`summary` of Post ",allow_null=True,required=False, allow_blank=True)
    published_at = serializers.CharField(help_text="`published_at` of Post ",allow_null=True,required=False, allow_blank=True)
    tags = serializers.ListField(child=serializers.IntegerField(help_text="list tags of Post"), allow_null=True,required=False)
    categories = serializers.ListField(child=serializers.IntegerField(help_text="list category of Post"), allow_null=True,required=False)
    thumbnail = serializers.CharField(help_text="`thumbnail` of Post ",allow_null=True,required=False, allow_blank=True)


    @staticmethod
    def validate(data):
        error = []

        if "parent" in data:
            parent = data["parent"]
            if parent is not None:
                parent = Post.objects.filter(id = parent).first()
                if not parent:
                    raise serializers.ValidationError("parent do not exist!")

        if "published_at" in data:
            published_at = data["published_at"]
            try:
                published_at = '{} 00:00:00'.format(published_at, '%d/%m/%Y %H:%M:%S')
                published_at = datetime.strptime(published_at, '%d/%m/%Y %H:%M:%S')
            except:
                raise serializers.ValidationError("published_at type is date %d/%m/%Y")
            data["published_at"] = published_at
        
        if "tags" in data:
            tags = data["tags"]
            if not isinstance(tags, list):
                raise serializers.ValidationError("tags must be array []!")
            if len(tags):
                list_tags = Category.objects.filter(id__in = tags)
                if len(list_tags) != len(tags):
                    raise serializers.ValidationError("some category is not exist or duplicate!")
                
           
        if "categories" in data:
            categories = data["categories"]
            if not isinstance(tags, list):
                raise serializers.ValidationError("categories must be array []!")
            if len(categories):
                list_category = Category.objects.filter(id__in = categories)
                if len(list_category) != len(categories):
                    raise serializers.ValidationError("some category is not exist or duplicate!")
            
        return data
