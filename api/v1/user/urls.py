from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from api.v1.user.views import RegisterAPI

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('token-verify/', TokenVerifyView.as_view()),
    path('register/', RegisterAPI.as_view()),
]