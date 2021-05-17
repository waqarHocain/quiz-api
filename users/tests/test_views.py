from django.contrib.auth import get_user_model
from django.urls import reverse
import pytest

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
