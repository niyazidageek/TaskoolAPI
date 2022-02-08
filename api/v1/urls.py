from django.urls import path, include

urlpatterns = [
    path('option/', include('api.v1.option.urls')),
    path('question/', include('api.v1.question.urls')),
    path('user/', include('api.v1.user.urls')),
    path('answer/', include('api.v1.answer.urls')),
]