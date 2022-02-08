from rest_framework import serializers
from taskool.models import Option, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

class OptionSerializer(serializers.ModelSerializer):
    deleteable_files = serializers.ListField(child=serializers.IntegerField(), required=False)
    file_content = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Option
        fields = "__all__"
        extra_kwargs = {
            "file_content": {
                "required": False,
            }
        }
