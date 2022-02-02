from rest_framework import serializers
from taskool.models import Question
from ..option.serializer import OptionSerializer


class QuestionSerializer(serializers.ModelSerializer):
    # options = OptionSerializer(source='option_set')
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"