from rest_framework import serializers
from taskool.models import Quiz


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = "__all__"
