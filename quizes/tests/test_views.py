from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest
from rest_framework.authtoken.models import Token

from quizes.views import QuizListCreate
from quizes.models import Quiz, Question, Answer

User = get_user_model()


@pytest.mark.django_db
class TestQuizListCreate:
    def setup_class(self):
        self.url = reverse("quizes:quizes_list")

    def setup_method(self):
        self.user = User.objects.create_user(email="a@b.com", password="aasdfew23")
        self.token = Token.objects.get(user=self.user)
        self.auth_header_str = f"Token {self.token.key}"

    def test_can_only_be_accessed_by_authorized_user(self, client):
        """Can only be accessed with a valid auth token"""
        response = client.get(self.url)
        assert response.status_code == 401

        # can be accessed with a valid token
        response2 = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)
        assert response2.status_code == 200

    def test_GET_request_returns_all_quizzes_for_logged_in_user(self, client):
        Quiz.objects.create(title="quiz1", user=self.user)
        Quiz.objects.create(title="quiz2", user=self.user)

        user2 = User.objects.create_user(email="foo@bar.com", password="sekoret321")
        Quiz.objects.create(title="quiz3", user=user2)

        response = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0].get("title") == "quiz1"
        assert response["Content-Type"] == "application/json"

    def test_POST_request_creates_a_new_quiz(self, client):
        response = client.post(
            self.url,
            HTTP_AUTHORIZATION=self.auth_header_str,
            data={"title": "New Quiz"},
        )

        assert response.status_code == 201
        assert response.data["title"] == "New Quiz"


@pytest.mark.django_db
class TestQuizDetail:
    def setup_method(self):
        self.user = User.objects.create_user(email="a@b.com", password="aasdfew23")
        self.quiz = Quiz.objects.create(title="test", user=self.user)
        self.token = Token.objects.get(user=self.user)
        self.auth_header_str = f"Token {self.token.key}"
        self.url = reverse("quizes:quiz_detail", args=[self.quiz.pk])

    def test_can_only_be_accessed_by_authorized_user(self, client):
        """Can only be accessed with a valid auth token"""
        response = client.get(self.url)
        assert response.status_code == 401

        # can be accessed with a valid token
        response2 = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)
        assert response2.status_code == 200

    def test_retrieves_the_detail_of_quiz(self, client):
        response = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)

        assert response.data["title"] == self.quiz.title

    def test_retrieves_all_questions_that_belong_to_quiz(self, client):
        Question.objects.create(title="Question 1", quiz=self.quiz)
        Question.objects.create(title="Question 2", quiz=self.quiz)
        response = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)

        assert len(response.data["questions"]) == 2
        response.data["questions"] == "Question 1"

    def test_DELETE_request_deletes_the_quiz(self, client):
        assert Quiz.objects.count() == 1
        client.delete(self.url, HTTP_AUTHORIZATION=self.auth_header_str)
        assert Quiz.objects.count() == 0

    def test_returns_404_if_provided_pk_is_wrong(self, client):
        incorrect_url = reverse("quizes:quiz_detail", args=[2])
        response = client.get(incorrect_url, HTTP_AUTHORIZATION=self.auth_header_str)

        assert response.status_code == 404
        assert "Not found" in response.data["detail"]


@pytest.mark.django_db
class TestQuestions:
    def setup_method(self):
        self.user = User.objects.create_user(email="a@b.com", password="aasdfew23")
        self.token = Token.objects.get(user=self.user)
        self.auth_header_str = f"Token {self.token.key}"
        self.quiz = Quiz.objects.create(title="test", user=self.user)
        self.url = reverse("quizes:questions", args=[self.quiz.id])

    def test_can_only_be_accessed_by_authorized_user(self, client):
        """Can only be accessed with a valid auth token"""
        response = client.get(self.url)
        assert response.status_code == 401

        # can be accessed with a valid token
        response2 = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)
        assert response2.status_code == 200

    def test_get_request_returns_all_created_questions_that_belong_to_specified_quiz_only(
        self, client
    ):
        quiz2 = Quiz.objects.create(title="quiz2", user=self.user)
        Question.objects.create(title="Shouldn't return", quiz=quiz2)

        Question.objects.create(title="Question 1", quiz=self.quiz)
        Question.objects.create(title="Question 2", quiz=self.quiz)

        response = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_post_request_creates_new_question_in_correct_quiz(self, client):
        response = client.post(
            self.url,
            HTTP_AUTHORIZATION=self.auth_header_str,
            data={"title": "Question 1"},
        )

        assert response.status_code == 201


@pytest.mark.django_db
class TestAnswerListCreate:
    def setup_method(self):
        self.user = User.objects.create_user(email="a@b.com", password="aasdfew23")
        self.quiz = Quiz.objects.create(title="quiz 1", user=self.user)
        self.question = Question.objects.create(title="question 1", quiz=self.quiz)
        self.token = Token.objects.get(user=self.user)
        self.auth_header_str = f"Token {self.token.key}"
        self.url = reverse(
            "quizes:answers",
            args=[self.quiz.id, self.question.id],
        )

    def test_GET_retrieves_all_answers_of_specified_questoin(self, client):
        Answer.objects.create(title="answer 1", question=self.question)
        Answer.objects.create(title="answer 2", correct=True, question=self.question)

        response = client.get(self.url, HTTP_AUTHORIZATION=self.auth_header_str)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[1].get("title") == "answer 2"

    def test_POST_request_creates_a_new_answer(self, client):
        response = client.post(
            self.url,
            HTTP_AUTHORIZATION=self.auth_header_str,
            data={"title": "new answer"},
        )

        assert response.status_code == 201
        assert response.data.get("title") == "new answer"
        assert response.data.get("question") == self.question.id
