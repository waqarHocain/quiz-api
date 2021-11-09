from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from . import models


class Answer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ["id", "title", "question", "correct"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Answer.objects.all(), fields=["title", "question"]
            )
        ]


class Question(serializers.ModelSerializer):
    answers = Answer(read_only=True, many=True, source="answer_set")

    class Meta:
        model = models.Question
        fields = ["id", "title", "quiz", "answers"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Question.objects.all(), fields=["title", "quiz"]
            )
        ]


class Quiz(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    questions = Question(read_only=True, many=True, source="question_set")

    class Meta:
        model = models.Quiz
        fields = ["id", "title", "user", "questions"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Quiz.objects.all(), fields=["title", "user"]
            )
        ]

    def save(self, **kwargs):
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)
