import pytest
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory

from quizes import serializers
from quizes import models

User = get_user_model()


@pytest.mark.django_db
class TestQuizSerializer:
    def setup_method(self):
        self.user = User.objects.create_user(email="foo@bar.com", password="jfklosoi32")
        self.request_factory = APIRequestFactory()
        self.request_factory.user = self.user

    def test_creates_quiz_object_when_saved(self):
        quiz_serializer = serializers.Quiz(
            data={"title": "test question"}, context={"request": self.request_factory}
        )
        assert quiz_serializer.is_valid()
        quiz_serializer.save()

        assert models.Quiz.objects.count() == 1

    def test_user_is_automatically_set_to_logged_in_user(self):
        quiz_serializer = serializers.Quiz(
            data={"title": "test question"}, context={"request": self.request_factory}
        )

        assert quiz_serializer.is_valid()
        quiz_serializer.save()
        assert models.Quiz.objects.count() == 1

    def test_does_NOT_save_when_duplicate_quiz_title_is_given(self):
        models.Quiz.objects.create(title="test title", user=self.user)
        quiz_serializer = serializers.Quiz(
            data={"title": "test title"}, context={"request": self.request_factory}
        )
        assert quiz_serializer.is_valid() == False

    def test_also_retrieves_all_associated_questions(self):
        quiz_serializer = serializers.Quiz(
            data={"title": "test title 0x01"}, context={"request": self.request_factory}
        )
        quiz_serializer.is_valid()
        quiz = quiz_serializer.save()
        models.Question.objects.create(title="question 1", quiz=quiz)
        models.Question.objects.create(title="question 2", quiz=quiz)

        assert len(quiz_serializer.data["questions"]) == 2
        assert quiz_serializer.data["questions"][0]["title"] == "question 1"


@pytest.mark.django_db
class TestQuestionSerializer:
    def test_creates_question_object_when_saved(self):
        user = User.objects.create_user(email="foo@bar.com", password="jfklosoi32")
        quiz = models.Quiz.objects.create(title="test quiz", user=user)
        question_serializer = serializers.Question(
            data={"title": "test question", "quiz": quiz.id}
        )

        assert question_serializer.is_valid()
        question_serializer.save()

        assert models.Question.objects.count() == 1

    def test_duplicate_questions_cannot_be_added_to_same_quiz(self):
        user = User.objects.create_user(email="foo@bar.com", password="jfklosoi32")
        quiz = models.Quiz.objects.create(title="test quiz", user=user)
        models.Question.objects.create(title="question", quiz=quiz)
        question_serializer = serializers.Question(
            data={"title": "question", "quiz": quiz.id}
        )

        assert question_serializer.is_valid() == False


@pytest.mark.django_db
class TestAnswerSerializer:
    def test_creates_answer_object_when_saved(self):
        user = User.objects.create_user(email="foo@bar.com", password="jfklosoi32")
        quiz = models.Quiz.objects.create(title="test quiz", user=user)
        question = models.Question.objects.create(title="question", quiz=quiz)
        answer_serializer = serializers.Answer(
            data={"title": "test answer", "question": question.id}
        )

        assert answer_serializer.is_valid()
        answer_serializer.save()

        assert models.Answer.objects.count() == 1

    def test_duplicate_answers_cannot_be_added_to_same_question(self):
        user = User.objects.create_user(email="foo@bar.com", password="jfklosoi32")
        quiz = models.Quiz.objects.create(title="test quiz", user=user)
        question = models.Question.objects.create(title="question", quiz=quiz)
        models.Answer.objects.create(title="answer", question=question)
        answer_serializer = serializers.Answer(
            data={"title": "answer", "question": question.id}
        )

        assert answer_serializer.is_valid() == False
