import collections
from collections import OrderedDict

from requests import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.v1.user.serializer import RegisterSerializer
from django.contrib.auth.models import Group


class RegisterStudentAPI(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        student_group = Group.objects.get(name='Student')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.get('groups').append(student_group)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)


class RegisterTeacherAPI(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        teacher_group = Group.objects.get(name='Teacher')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.get('groups').append(teacher_group)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)