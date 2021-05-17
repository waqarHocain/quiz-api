from django.contrib.auth import get_user_model
import pytest

from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.mark.django_db
class TestUserManager:
    def test_create_user_with_email_and_password_only(self):
        user = User.objects.create_user(email="a@b.com", password="sekrti12#2")
        assert User.objects.count() == 1
        assert user.email == "a@b.com"

    def test_create_user_raise_error_if_email_not_provided(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email="", password="asjeiwo2")

    def test_a_token_is_created_when_creating_a_new_user(self):
        user = User.objects.create_user(email="a@b.com", password="sekrti12#2")
        token = Token.objects.get(user=user)

    def test_password_is_set_properly(self):
        password = "sekrti12#2"
        user = User.objects.create_user(email="a@b.com", password=password)
        assert user.password != password

    def test_create_superuser_sets_admin_to_true(self):
        user = User.objects.create_superuser(email="a@b.com", password="sekdasfs32")
        assert user.is_admin == True


@pytest.mark.django_db
class TestUser:
    def test_user_is_active_by_default(self):
        user = User.objects.create_user(email="a@b.com", password="sekrti12#2")
        assert user.is_active == True

    def test_user_is_NOT_admin_by_default(self):
        user = User.objects.create_user(email="a@b.com", password="sekdasfs32")
        assert user.is_admin == False

    def test_user_is_NOT_staff_by_default(self):
        user = User.objects.create_user(email="a@b.com", password="sekrti12#2")
        assert user.is_staff == False
