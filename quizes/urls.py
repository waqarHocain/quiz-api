from django.urls import path

from . import views

app_name = "quizes"
urlpatterns = [
    path("", views.QuizListCreate.as_view(), name="quizes_list"),
    path("<int:pk>/", views.QuizDetail.as_view(), name="quiz_detail"),
]
