from django.contrib.auth import get_user_model
import pytest

from users.serializers import UserSerializer

User = get_user_model()


@pytest.mark.django_db
class TestUserSerializer:
    def test_creates_a_new_User_object_in_database_with_valid_data(self):
        data = {"email": "a@b.com", "password": "sekfritj13"}
        user_serializer = UserSerializer(data=data)
        assert user_serializer.is_valid()
        user_serializer.save()
        assert User.objects.filter(**user_serializer.data).exists()

    def test_raise_error_when_invalid_email_is_passed(self):
        data = {"email": "abcomdjfk", "password": "sekfritj13"}
        user_serializer = UserSerializer(data=data)
        assert user_serializer.is_valid() == False

    def test_password_minimum_length_is_8_characters(self):
        data = {"email": "a@b.com", "password": "1234567"}
        user_serializer = UserSerializer(data=data)
        assert user_serializer.is_valid() == False

    def test_password_is_write_only_field(self):
        data = {"email": "a@b.com", "password": "asdfer232"}
        user_serializer = UserSerializer(data=data)
        assert user_serializer.is_valid()
        assert "password" not in user_serializer.data

    def test_password_is_NOT_saved_in_plaintext(self):
        data = {"email": "a@b.com", "password": "asdfer232"}
        user_serializer = UserSerializer(data=data)
        assert user_serializer.is_valid()
        user = user_serializer.save()
        assert user.password != data["password"]
