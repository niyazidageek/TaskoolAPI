from django.urls import path
from . import views

urlpatterns=[
    path('', views.QuestionAPI.as_view()),
    path('<int:pk>', views.QuestionRetrieveUpdateDestroyAPI.as_view()),
    path('file', views.QuestionFileAPI.as_view()),
    path('file/<int:pk>', views.QuestionFileRetrieveUpdateDestroyAPI.as_view()),
]