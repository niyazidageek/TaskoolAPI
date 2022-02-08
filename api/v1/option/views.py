from rest_framework import status
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from taskool.models import Option, File
from rest_framework.permissions import AllowAny
from . import serializer


class OptionAPI(ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = serializer.OptionSerializer
    permission_classes = (AllowAny,)
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        files = request.FILES.getlist('file_content')

        if files:
            request.data.pop('file_content')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                option_qs = Option.objects.get(id=serializer.data['id'])
                uploaded_files=[]
                for file in files:
                    content = File.objects.create(media=file, extension=file.__getattribute__('content_type'))
                    uploaded_files.append(content)

                    option_qs.file_content.add(*uploaded_files)
                    context = serializer.data
                    context["file_content"] = [file.id for file in uploaded_files]
                    return Response(context, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"status": True,
                             "message": "Option added",
                             "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class OptionRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.OptionSerializer

    def get_queryset(self):
        return Option.objects.filter(id=self.kwargs.get('pk', None))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response({"status":True,"message":"Option updated!", "data":serializer.data})


