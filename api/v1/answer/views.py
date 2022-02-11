from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveDestroyAPIView)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from taskool.models import Option, File, Answer, TextAnswer, AudioAnswer
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from . import serializer


class AnswerAPI(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = serializer.AnswerSerializer
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'question__quiz_id']

    def create(self, request, *args, **kwargs):
        text_answer = request.data.get('text_answer')
        audio_answer = request.data.get('audio_answer')
        request.data._mutable = True

        if text_answer:
            text_answer_db = TextAnswer.objects.create(text=text_answer)
            request.data.update({'text_answer_id':text_answer_db.__getattribute__('id')})

        if audio_answer:
            audio_answer_db = AudioAnswer.objects.create(media=audio_answer)
            request.data['audio_answer_id'] = audio_answer_db.__getattribute__('id')

        request.data['user'] = request.user.id
        request.data._mutable = False

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True,
                         "message": "Option added",
                         "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class AnswerRetrieveDestroyAPI(RetrieveDestroyAPIView):
    serializer_class = serializer.AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(id=self.kwargs.get('pk', None))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.file_content.all():
            for file in instance.file_content.all():
                file.media.delete()
        self.perform_destroy(instance)
        return Response({"status": True, "message": "Option deleted!"})


