from models.category.models import Category
from models.post.models import Post
from models.tag.models import Tag
from models.user.models import User
from rest_framework import serializers
from datetime import datetime

class ListPostSerializer(serializers.Serializer):
    detail = serializers.IntegerField(help_text="Detail tags and categories of post",required=False,allow_null=True)
    is_pagination = serializers.IntegerField(help_text="Pagination of post",required=False,allow_null=True)
    keyword = serializers.CharField(help_text="keyword of post",required=False,allow_null=True, allow_blank=True)
    tag = serializers.IntegerField(help_text="tag of post",required=False,allow_null=True)
    category = serializers.IntegerField(help_text="category of post",required=False,allow_null=True)
    author = serializers.IntegerField(help_text="Author of post",required=False,allow_null=True)

    @staticmethod
    def validate(data):
        error = []
        if "detail" in data:
            detail = data["detail"]
            if detail not in [0,1]:
                raise serializers.ValidationError("detail must be in [0,1]!")

        if "is_pagination" in data:
                    detail = data["is_pagination"]
                    if detail not in [0,1]:
                        raise serializers.ValidationError("is_pagination must be in [0,1]!")

        if "tag" in data:
            tag = data["tag"]
            if tag:
                tag = Tag.objects.filter(id = tag)
                if not tag:
                    raise serializers.ValidationError("Tag is not exist!")

        if "category" in data:
            category = data["category"]
            if category:
                category = Category.objects.filter(id = category)
                if not category:
                    raise serializers.ValidationError("Category is not exist!")

        return data
    
class ListPostRelationSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(help_text="id of post",required=False,allow_null=True)
    tags = serializers.ListField(child=serializers.IntegerField(help_text="list tags of Post"), allow_null=True,required=False)
    categories = serializers.ListField(child=serializers.IntegerField(help_text="list category of Post"), allow_null=True,required=False)

    @staticmethod
    def validate(data):
        error = []
        if not "post_id" in data:
            raise serializers.ValidationError("post id is required")
        else:
            post_id =  data["post_id"]
            post =Post.objects.filter(id = post_id).first()
            if not post:
                raise serializers.ValidationError("post do not exist")

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

class ListPostByAuthorSerializer(serializers.Serializer):
    detail = serializers.IntegerField(help_text="Detail tags and categories of post",required=False,allow_null=True)

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
                published_at = '{}'.format(published_at, '%d/%m/%Y %H:%M:%S')
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
                published_at = '{}'.format(published_at, '%d/%m/%Y %H:%M:%S')
                published_at = datetime.strptime(published_at, '%d/%m/%Y %H:%M:%S')
            except:
                raise serializers.ValidationError("published_at type is date %d/%m/%Y")
            data["published_at"] = published_at
        
        if "tags" in data:
            tags = data["tags"]
            if not isinstance(tags, list):
                raise serializers.ValidationError("tags must be array []!")
            if len(tags):
                list_tags = Tag.objects.filter(id__in = tags)
                if len(list_tags) != len(tags):
                    raise serializers.ValidationError("some tags is not exist or duplicate!")
                
           
        if "categories" in data:
            categories = data["categories"]
            if not isinstance(tags, list):
                raise serializers.ValidationError("categories must be array []!")
            if len(categories):
                list_category = Category.objects.filter(id__in = categories)
                if len(list_category) != len(categories):
                    raise serializers.ValidationError("some category is not exist or duplicate!")
            
        return data
