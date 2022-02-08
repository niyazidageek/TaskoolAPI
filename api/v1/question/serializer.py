from rest_framework import serializers
from taskool.models import Question
from ..option.serializer import OptionSerializer, FileSerializer


class QuestionSerializer(serializers.ModelSerializer):
    deleteable_files = serializers.ListField(child=serializers.IntegerField(), required=False)
    file_content = FileSerializer(many=True, read_only=True)
    option_set = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            "file_content": {
                "required": False,
            }
        }