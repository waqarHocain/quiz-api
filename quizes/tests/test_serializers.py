import pytest
from django.contrib.auth import get_user_model

from quizes import serializers
from quizes import models

User = get_user_model()


@pytest.mark.django_db
class TestQuizSerializer:
    def test_creates_quiz_object_when_saved(self):
        user = User.objects.create_user(email="foo@bar.com", password="jfklosoi32")
        quiz_serializer = serializers.Quiz(
            data={"title": "test question", "user": user.id}
        )
        assert quiz_serializer.is_valid()
        quiz_serializer.save()

        assert models.Quiz.objects.count() == 1

    def test_does_NOT_save_when_duplicate_quiz_title_is_given(self):
        user = User.objects.create_user(email="foo@bar.com", password="jfklosoi32")
        models.Quiz.objects.create(title="test title", user=user)
        quiz_serializer = serializers.Quiz(
            data={"title": "test title", "user": user.id}
        )
        assert quiz_serializer.is_valid() == False


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
