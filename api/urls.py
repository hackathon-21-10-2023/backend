from django.urls import path, include, re_path
from . import views


urlpatterns = [
    path('list_slaves_of_head/<int:pk>/', views.SlavesListForItsHead.as_view()),
]
