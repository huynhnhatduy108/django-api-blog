from rest_framework import serializers

class CreatePostMetaSerializer(serializers.Serializer):
    post = serializers.IntegerField(help_text="`task_type` of Category ",required=False, allow_null=True)
    content = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)
    key = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
        return data

class UpdatePostMetaSerializer(serializers.Serializer):
    post = serializers.IntegerField(help_text="`task_type` of Category ",required=False, allow_null=True)
    content = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)
    key = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
        return data