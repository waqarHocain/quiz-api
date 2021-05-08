import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from quizes.models import Quiz

User = get_user_model()


@pytest.mark.django_db
class TestQuiz:
    def test_same_user_can_create_many_quizes(self):
        user = User.objects.create_user(email="a@b.com", password="sekrit12")
        quiz1 = Quiz.objects.create(title="New quiz", user=user)
        quiz2 = Quiz.objects.create(title="Fresh quiz", user=user)

        assert len(user.quiz_set.all()) == 2

    def test_quiz_title_is_unique_per_user(self):
        """Quiz title and user are unique together"""
        user = User.objects.create_user(email="a@b.com", password="sekrit12")
        Quiz.objects.create(title="New quiz", user=user)
        with pytest.raises(IntegrityError):
            Quiz.objects.create(title="New quiz", user=user)

    def test_str_returns_quiz_title(self):
        user = User.objects.create_user(email="a@b.com", password="sekrit12")
        quiz = Quiz.objects.create(title="New quiz", user=user)
        assert str(quiz) == "New quiz"
