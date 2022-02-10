from rest_framework import serializers
from rest_framework import serializers
from api.v1.option.serializer import OptionSerializer
from taskool.models import AudioAnswer, Answer, TextAnswer


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnswer
        fields = "__all__"


class TextAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextAnswer
        fields = "__all__"


class AudioAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AudioAnswer
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    text_answer_id = serializers.IntegerField(write_only=True, required=False)
    audio_answer_id = serializers.IntegerField(write_only=True, required=False)
    text_answer = TextAnswerSerializer(read_only=True)
    audio_answer = AudioAnswerSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = "__all__"
