import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from quizes.models import Quiz, Question, Answer

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


@pytest.mark.django_db
class TestQuestion:
    def setup_method(self):
        self.user = User.objects.create_user(email="a@b.com", password="sekrit12")
        self.quiz = Quiz.objects.create(title="New quiz", user=self.user)
        self.question = Question.objects.create(
            title="What's in the name?", quiz=self.quiz
        )

    def test_many_questions_can_be_added_to_a_quiz(self):
        question2 = Question.objects.create(title="Question 2", quiz=self.quiz)
        assert len(self.quiz.question_set.all()) == 2

    def test_question_title_is_unique_in_a_quiz(self):
        # question with below title already exists in db, so it SHOULD raise error
        duplicate_title = self.question.title
        with pytest.raises(IntegrityError):
            Question.objects.create(title=duplicate_title, quiz=self.quiz)

    def test_str_returns_question_title(self):
        assert str(self.question) == self.question.title


@pytest.mark.django_db
class TestAnswer:
    def setup_method(self):
        self.user = User.objects.create_user(email="a@b.com", password="sekrit12")
        self.quiz = Quiz.objects.create(title="New quiz", user=self.user)
        self.question = Question.objects.create(
            title="What's in the name?", quiz=self.quiz
        )
        self.answer = Answer.objects.create(title="test answer", question=self.question)

    def test_many_answers_can_be_added_to_a_question(self):
        Answer.objects.create(title="answer 2", question=self.question)
        assert len(self.question.answer_set.all()) == 2

    def test_answer_is_NOT_correct_by_default(self):
        assert self.answer.correct == False

    def test_two_duplicate_answers_CANNOT_be_added_to_a_question(self):
        with pytest.raises(IntegrityError):
            Answer.objects.create(title="test answer", question=self.question)

    def test_str_returns_answer_title(self):
        assert str(self.answer) == "test answer"
