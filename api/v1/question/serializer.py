from rest_framework import serializers
from taskool.models import Question
from ..option.serializer import OptionSerializer, QuestionFileSerializer


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    files = QuestionFileSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'