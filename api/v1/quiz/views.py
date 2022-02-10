from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
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


class QuizRetrieveUpdateDestroyAPI(RetrieveUpdateDestroyAPIView):
        serializer_class = serializer.QuizSerializer

        def get_queryset(self):
            return Quiz.objects.filter(id=self.kwargs.get('pk', None))

        def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response({"status": True, "message": "Quiz updated!", "data": serializer.data})
