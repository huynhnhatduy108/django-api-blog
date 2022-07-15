from rest_framework import serializers

class SearchCategorySerializer(serializers.Serializer):
    keyword = serializers.CharField(help_text="Detail tags and categories of post",required=False,allow_null=True, allow_blank=True,)
    @staticmethod
    def validate(data):
        return data

class CreateCategorySerializer(serializers.Serializer):
    parent = serializers.IntegerField(help_text="`task_type` of Task ",required=False, allow_null=True)
    title = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)
    meta_title = serializers.CharField(help_text="`meta_title` of Category ",allow_null=True,allow_blank=True,required=False)
    description = serializers.CharField(help_text="`description` of Category ",allow_null=True,allow_blank=True,required=False)
    thumbnail = serializers.CharField(help_text="`thumbnail` of Post ",allow_null=True,required=False, allow_blank=True)

    @staticmethod
    def validate(data):
        return data


class UpdateCategorySerializer(serializers.Serializer):
    parent = serializers.IntegerField(help_text="`task_type` of Task ",required=False, allow_null=True)
    title = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)
    meta_title = serializers.CharField(help_text="`meta_title` of Category ",allow_null=True,allow_blank=True,required=False)
    description = serializers.CharField(help_text="`description` of Category ",allow_null=True,allow_blank=True,required=False)
    thumbnail = serializers.CharField(help_text="`thumbnail` of Post ",allow_null=True,required=False, allow_blank=True)

    @staticmethod
    def validate(data):
        return data
