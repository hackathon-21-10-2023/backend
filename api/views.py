from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes

from api.serializers import UserSerializer
from . import models
from .models import User


@api_view()
@permission_classes([permissions.AllowAny])
def health_check_view(request):
    return Response({"health": "OK"})


class SlavesListForItsHead(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        head_id = self.kwargs['pk']
        head = get_object_or_404(User, pk=head_id)
        if not head.is_head:
            return Response(status=403, data={"detail": "Not a head"})

        head_department = head.department
        if not head.department:
            return Response(status=404, data={"detail": "Department not found for head"})

        slaves_and_head_in_department = User.objects.filter(department=head_department)
        slaves_in_department = slaves_and_head_in_department.exclude(pk=head.pk)
        return self.serializer_class(slaves_in_department)
