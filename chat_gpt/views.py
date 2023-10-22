from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Feedback, FeedbackItem, User
from chat_gpt.services import generate_text


class AskGPTReview(APIView):
    def post(self, request, employee_id):
        employee = User.objects.filter(id=employee_id).last()

        if not employee:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"details": "this employee does not exist!"})
        if employee.is_reviewed_by_gpt:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"details": "this feedback already reviewed!"})

        text = generate_text(feedback)
        print(text)
        return Response({"text": text})
