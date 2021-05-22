from rest_framework import generics

from .models import Quiz
from . import serializers


class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = serializers.Quiz

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
