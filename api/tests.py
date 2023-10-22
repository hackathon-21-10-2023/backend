from django.contrib.auth import get_user_model
from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory,
)

from api.models import User, Department


class APITest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.department = Department.objects.create(name="python")
        print(self.department)

        self.common_user_default_1 = User.objects.create_user(email='aaaa@aa.com', password='123', name='aaa',
                                                              surname='aaa', username="1",
                                                              department=self.department, position="Джун")
        self.common_user_default_2 = User.objects.create_user(email='aaaa2@aa.com', password='123', name='aaa2', surname='aaa',
                                                              department='python', position="Джун", username="2")

        self.common_user_default_3 = User.objects.create_user(email='aaaa3@aa.com', password='123', name='aaa3', surname='aaa',
                                                              department=self.department, position="Джун", username="3")
        self.common_user_head = User.objects.create_user(email='bosss@bb.com', password='123', name='bbb', surname='bbb',
                                                              department=self.department, position="Тимлид", is_head=True, username="4")
        self.common_user_intern = User.objects.create_user(email='intern@cc.com', password='123', name='ccc', surname='ccc',
                                                      department=self.department, position="Стажер", is_intern=True, username="5")

    def test_check_if_employeers_created(self):
        self.assertEqual(User.objects.count(), 5)





