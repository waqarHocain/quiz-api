from django.urls import path

from . import views


app_name = "auth"

urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
]
