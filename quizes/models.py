from django.db import models
from django.contrib.auth import get_user_model


class Quiz(models.Model):
    title = models.CharField(max_length=254)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "user"], name="unique_title")
        ]

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=400)
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "quiz"], name="unique_question_title"
            )
        ]

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=400)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "question"], name="unique_answer_title"
            )
        ]

    def __str__(self):
        return self.title
