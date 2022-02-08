from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from taskool.models import Question, File
from rest_framework.permissions import AllowAny
from . import serializer


class QuestionAPI(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializer.QuestionSerializer
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request, *args, **kwargs):

        print(request.user.id)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file_content')
        if files:
            request.data.pop('file_content')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                question_qs = Question.objects.get(id=serializer.data['id'])
                uploaded_files=[]
                for file in files:
                    content = File.objects.create(media=file, extension=file.__getattribute__('content_type'))
                    uploaded_files.append(content)

                question_qs.file_content.add(*uploaded_files)
                context = serializer.data
                context["file_content"] = [file.id for file in uploaded_files]
                return Response(context, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"status":True,
                             "message":"Question added",
                             "data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class QuestionRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.QuestionSerializer
    parser_classes = [MultiPartParser,FormParser]
    def get_queryset(self):
        return Question.objects.filter(id=self.kwargs.get('pk', None))

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
            question_qs = Question.objects.get(id=instance.id)
            uploaded_files = []
            for file in files:
                content = File.objects.create(media=file, extension=file.__getattribute__('content_type'))
                uploaded_files.append(content)

            question_qs.file_content.add(*uploaded_files)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"status": True, "message": "Question updated!", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.file_content.all():
            for file in instance.file_content.all():
                file.media.delete()
        self.perform_destroy(instance)
        return Response({"status": True, "message": "Question deleted!"})



