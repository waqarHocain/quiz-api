from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny

from . import serializers
from . import models


class Register(generics.CreateAPIView):
    """Creates a new user object provided valid email and password"""

    permission_classes = [AllowAny]
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class Login(ObtainAuthToken):
    """Given email/password of an existing user, returns back auth token and email"""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = Token.objects.get(user=user)
        return Response({"token": token.key, "email": user.email, "id": user.pk})
