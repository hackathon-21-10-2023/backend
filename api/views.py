from django.db import transaction
from django.db.models import Subquery
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from api.serializers import UserSerializer, MetricSerializer, FeedbackSerializer
from .exceptions import IsNotHeadError, DepartmentNotFoundError, NoHeadForDepartamentFoundError
from .models import User, WaitForReview, Metric, Feedback


@api_view()
@permission_classes([permissions.AllowAny])
def health_check_view(request):
    return Response({"health": "OK"})


class SlavesListForItsHead(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        head_id = self.kwargs.get('pk', None)
        if head_id is None:
            raise ValidationError("No id of head was provided")
        head = get_object_or_404(User, pk=head_id)

        try:
            queryset = head.slaves_for_head
        except IsNotHeadError:
            raise PermissionDenied("Only head can list slaves")
        except DepartmentNotFoundError:
            raise PermissionDenied("Department not found for head")
        return queryset


class AskReview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)

        user.is_awaiting_feedback = True
        try:
            reviewers = user.reviewers
        except NoHeadForDepartamentFoundError:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"detail": "Department not found for head for this intern"})

        if len(reviewers) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"detail": "Not for any reviewer"})

        with transaction.atomic():
            user_to_review, _ = WaitForReview.objects.get_or_create(to_user=user)
            user_to_review.from_users.set(reviewers)
            user.save()

        serializer = self.serializer_class(reviewers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetMe(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ListNeedToReviewUsers(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        subquery = WaitForReview.objects.filter(from_users=self.request.user).values('to_user__pk')
        queryset = User.objects.exclude(pk=self.request.user.pk).filter(pk=Subquery(subquery))
        return queryset


class MetricListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MetricSerializer

    def get_queryset(self):
        return Metric.objects.all()


class ReviewListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        employee_id = self.kwargs.get('employee_id', None)
        if not employee_id:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"detail": "Employee id was not passed!"})
        employee = User.objects.filter(id=employee_id).last()
        if not employee:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={"detail": "This employee does not exist!"})

        return Feedback.objects.filter(to_user=employee)
