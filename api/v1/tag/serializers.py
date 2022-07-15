from rest_framework import serializers

class SearchTagSerializer(serializers.Serializer):
    keyword = serializers.CharField(help_text="Detail tags and categories of post",required=False,allow_null=True, allow_blank=True,)
    @staticmethod
    def validate(data):
        return data

class CreateTagSerializer(serializers.Serializer):
    title = serializers.CharField(help_text="`title` of Tag ",allow_null=True,allow_blank=True,required=False)
    meta_title = serializers.CharField(help_text="`meta_title` of Tag ",allow_null=True,allow_blank=True,required=False)
    description = serializers.CharField(help_text="`description` of Tag ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
        return data

class UpdateTagSerializer(serializers.Serializer):
    title = serializers.CharField(help_text="`title` of Tag ",allow_null=True,allow_blank=True,required=False)
    meta_title = serializers.CharField(help_text="`meta_title` of Tag ",allow_null=True,allow_blank=True,required=False)
    description = serializers.CharField(help_text="`description` of Tag ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
        return data