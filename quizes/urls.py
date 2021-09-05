from django.urls import path

from . import views

app_name = "quizes"
urlpatterns = [
    path("", views.QuizListCreate.as_view(), name="quizes_list"),
    path("<int:pk>/", views.QuizDetail.as_view(), name="quiz_detail"),
    path("<int:pk>/questions/", views.QuestionListCreate.as_view(), name="questions"),
    path(
        "<int:pk>/questions/<int:question_pk>",
        views.AnswerListCreate.as_view(),
        name="answers",
    ),
]
