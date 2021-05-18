from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from . import models


class Quiz(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Quiz
        fields = ["id", "title", "user"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Quiz.objects.all(), fields=["title", "user"]
            )
        ]

    def save(self, **kwargs):
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)


class Question(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ["id", "title", "quiz"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Question.objects.all(), fields=["title", "quiz"]
            )
        ]


class Answer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ["id", "title", "question", "correct"]
        validators = [
            UniqueTogetherValidator(
                queryset=models.Answer.objects.all(), fields=["title", "question"]
            )
        ]
