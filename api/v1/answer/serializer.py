from rest_framework import serializers
from taskool.models import AudioAnswer, Answer, TextAnswer


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnswer
        fields = "__all__"


class TextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextAnswer
        field = "__all__"


class AudioAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnswer
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    text_answer = TextAnswerSerializer
    audio_answer = AudioAnswerSerializer

    class Meta:
        model = Answer
        fields = "__all__"
