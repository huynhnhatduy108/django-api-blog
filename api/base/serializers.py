from rest_framework import serializers

class ExceptionResponseSerializer(serializers.Serializer):
    error_code = serializers.CharField(help_text="Unique code of this error")
    description = serializers.CharField(help_text="Detail description of this error")