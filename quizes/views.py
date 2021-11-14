from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Quiz, Question, Answer
from . import serializers


class QuizListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.Quiz

    def get_queryset(self):
        return Quiz.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuizDetail(generics.RetrieveDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = serializers.Quiz


class QuestionListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.Question

    def get_queryset(self):
        return Question.objects.filter(quiz__id=self.kwargs["pk"])

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.Question(
            data={"title": request.data.get("title"), "quiz": self.kwargs["pk"]}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AnswerListCreate(generics.ListCreateAPIView):
    serializer_class = serializers.Answer

    def get_queryset(self):
        return Answer.objects.filter(question__id=self.kwargs["question_pk"])

    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.Answer(
            data={
                "title": request.data.get("title"),
                "question": self.kwargs["question_pk"],
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
