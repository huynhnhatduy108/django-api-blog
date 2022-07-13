from rest_framework import serializers

class CreateCategorySerializer(serializers.Serializer):
    parent = serializers.IntegerField(help_text="`task_type` of Task ",required=False, allow_null=True)
    title = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)
    meta_title = serializers.CharField(help_text="`meta_title` of Category ",allow_null=True,allow_blank=True,required=False)
    description = serializers.CharField(help_text="`description` of Category ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
        return data


class UpdateCategorySerializer(serializers.Serializer):
    parent = serializers.IntegerField(help_text="`task_type` of Task ",required=False, allow_null=True)
    title = serializers.CharField(help_text="`title` of Category ",allow_null=True,allow_blank=True,required=False)
    meta_title = serializers.CharField(help_text="`meta_title` of Category ",allow_null=True,allow_blank=True,required=False)
    description = serializers.CharField(help_text="`description` of Category ",allow_null=True,allow_blank=True,required=False)

    @staticmethod
    def validate(data):
        return data
