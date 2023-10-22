from django.urls import path

from chat_gpt.views import AskGPTReview

urlpatterns = [
    path("create_review/<int:employee_id>/", AskGPTReview.as_view()),
]
