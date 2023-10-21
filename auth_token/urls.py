from django.urls import path, include

from .views import LoginByCredentials

urlpatterns = [
    path('login/', LoginByCredentials.as_view(), name='login'),
]