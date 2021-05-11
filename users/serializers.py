from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"min_length": 8, "write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
