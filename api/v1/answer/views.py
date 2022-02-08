from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from taskool.models import Option, File, Answer, TextAnswer, AudioAnswer
from rest_framework.permissions import AllowAny
from . import serializer


class AnswerAPI(ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = serializer.AnswerSerializer
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        text_answer = request.data.get('text_answer')
        audio_answer = request.data.get('audio_answer')

        if text_answer:
            text_answer_db = TextAnswer.objects.create(text=text_answer)
            request.data['text_answer'] = text_answer_db.__getattribute__('id')

        if audio_answer:
            audio_answer_db = AudioAnswer.objects.create(media=audio_answer)
            request.data['audio_answer'] = audio_answer_db.__getattribute__('id')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True,
                         "message": "Option added",
                         "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class OptionRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.AnswerSerializer

    def get_queryset(self):
        return Option.objects.filter(id=self.kwargs.get('pk', None))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('deleteable_files'):
            for fileId in serializer.validated_data.get('deleteable_files'):
                if any(fileId == efi.id for efi in instance.file_content.all()):
                    file = next((i for i in instance.file_content.all() if i.id == fileId))
                    file.media.delete()
                    file.delete()

        files = request.FILES.getlist('file_content')

        if files:
            request.data.pop('file_content')
            option_qs = Option.objects.get(id=instance.id)
            uploaded_files = []
            for file in files:
                content = File.objects.create(media=file, extension=file.__getattribute__('content_type'))
                uploaded_files.append(content)

            option_qs.file_content.add(*uploaded_files)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"status": True, "message": "Option updated!", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.file_content.all():
            for file in instance.file_content.all():
                file.media.delete()
        self.perform_destroy(instance)
        return Response({"status": True, "message": "Option deleted!"})


