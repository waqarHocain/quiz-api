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
