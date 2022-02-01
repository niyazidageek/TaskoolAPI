from django.urls import path
from . import views

urlpatterns=[
    path('', views.OptionAPI.as_view()),
    path('<int:pk>', views.OptionRetrieveUpdateDestroyAPI.as_view())
]