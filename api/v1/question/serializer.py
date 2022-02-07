from rest_framework import serializers
from taskool.models import Question
from ..option.serializer import OptionSerializer


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    deleteable_files = serializers.ListField(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Question
        fields = '__all__'
        depth = 1
        extra_kwargs = {
            "file_content": {
                "required": False,
            }
        }