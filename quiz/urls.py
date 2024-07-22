from django.urls import path, include
from .views import (
    CategoryList,
    QuizList,
    QuestionList,
    ResultsGetPost,
    PhotoViewSet
)
from rest_framework import routers
router=routers.DefaultRouter()
router.register('results',ResultsGetPost)
router.register(r'photos', PhotoViewSet)


urlpatterns = [
    path('home/', CategoryList.as_view()),
    path('quiz/', QuizList.as_view()),
    path('question/', QuestionList.as_view()),
    path('',include(router.urls)),
]