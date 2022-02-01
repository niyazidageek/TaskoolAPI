from django.urls import path, include

urlpatterns=[
    path('option/', include('api.v1.option.urls'))
]