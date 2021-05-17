from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest

from rest_framework.authtoken.models import Token

from users.views import Register

User = get_user_model()


@pytest.mark.django_db
class TestRegiseterView:
    def setup_class(self):
        self.url = reverse("auth:register")

    def test_POST_request_with_valid_data_creates_a_user_object_in_db(self, client):
        data = {"email": "a@b.com", "password": "sekrit123"}
        response = client.post(self.url, data)

        assert response.status_code == 201
        assert User.objects.filter(email=data["email"]).exists()

    def test_id_and_email_are_returned_back_in_response(self, client):
        data = {"email": "a@b.com", "password": "sekrit123"}
        response = client.post(self.url, data)

        assert response.status_code == 201
        assert response.data == {"id": 1, "email": data["email"]}

    def test_POST_request_with_invalid_email_does_NOT_create_user(self, client):
        data = {"email": "ab.com", "password": "sekrit123"}
        response = client.post(self.url, data)

        assert response.status_code == 400
        assert User.objects.count() == 0

    def test_POST_request_with_short_or_missing_password_does_NOT_create_user(
        self, client
    ):
        # short password, should be atleat 8 chars
        data = {"email": "a@b.com", "password": "sekrit"}
        response = client.post(self.url, data)

        # missing password
        data2 = {"email": "a@b.com", "password": ""}
        response2 = client.post(self.url, data)

        assert response.status_code == 400
        assert response2.status_code == 400
        assert User.objects.count() == 0


@pytest.mark.django_db
class TestLoginView:
    def setup_class(self):
        self.url = reverse("auth:login")

    def test_POST_request_with_valid_email_password_returns_back_token_and_email(
        self, client
    ):
        data = {"email": "a@b.com", "password": "sekrit123"}
        user = User.objects.create_user(**data)
        token = Token.objects.get(user=user)

        response = client.post(
            self.url, {"username": data["email"], "password": data["password"]}
        )

        assert response.status_code == 200
        assert response.data["token"] == token.key
        assert response.data["email"] == user.email

    def test_POSTing_invalid_data_returns_back_no_token(self, client):
        data = {"email": "a@b.com", "password": "sekrit123"}
        user = User.objects.create_user(**data)

        response = client.post(
            self.url, {"username": data["email"], "password": "wrongpassword420"}
        )

        assert response.status_code == 400
        assert "token" not in response.data
