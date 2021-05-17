from rest_framework import generics

from . import serializers
from . import models


class Register(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
