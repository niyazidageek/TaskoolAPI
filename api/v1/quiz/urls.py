from django.urls import path
from . import views

urlpatterns=[
    path('', views.QuizAPI.as_view()),
    path('<int:pk>', views.QuizRetrieveUpdateDestroyAPI.as_view()),
]