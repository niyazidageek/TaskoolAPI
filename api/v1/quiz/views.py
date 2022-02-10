from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from . import serializer
from taskool.models import Quiz


class QuizAPI(ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = serializer.QuizSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"status": True,
                         "message": "Quiz added",
                         "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)