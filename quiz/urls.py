from django.urls import path, include
from .views import (
    CategoryList,
    QuizList,
    QuestionList,
    ResultsGetPost
)
from rest_framework import routers
router=routers.DefaultRouter()
router.register('results',ResultsGetPost)



urlpatterns = [
    path('home/', CategoryList.as_view()),
    path('quiz/', QuizList.as_view()),
    path('question/', QuestionList.as_view()),
    path('',include(router.urls)),
]