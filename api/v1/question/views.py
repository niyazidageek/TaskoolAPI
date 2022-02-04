from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from taskool.models import Question, QuestionFile
from rest_framework.permissions import AllowAny
from . import serializer


class QuestionAPI(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializer.QuestionSerializer
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    def create(self, request, *args, **kwargs):
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

        # if serializer.validated_data.get('image'):
        #     if instance.image:
        #         instance.image.delete()
        # else:
        #     if instance.image:
        #         instance.image.delete()

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"status": True, "message": "Question updated!", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # if instance.image:
        #     instance.image.delete()
        self.perform_destroy(instance)
        return Response({"status":True,"message":"Question deleted!"})



class QuestionFileAPI(ListCreateAPIView):
    queryset = QuestionFile.objects.all()
    serializer_class = serializer.QuestionFileSerializer
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status" : True,
                         "message" : "Question file added",
                         "data" : serializer.data}, status=status.HTTP_201_CREATED, headers=headers)



class QuestionFileRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.QuestionFileSerializer
    parser_classes = [MultiPartParser,FormParser]
    def get_queryset(self):
        return QuestionFile.objects.filter(id=self.kwargs.get('pk', None))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # if serializer.validated_data.get('image'):
        #     if instance.image:
        #         instance.image.delete()
        # else:
        #     if instance.image:
        #         instance.image.delete()

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"status": True, "message": "Question file updated!", "data": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # if instance.image:
        #     instance.image.delete()
        self.perform_destroy(instance)
        return Response({"status":True,"message":"Question file deleted!"})






