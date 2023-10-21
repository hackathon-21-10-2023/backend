from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import QuerySet

from api.exceptions import IsNotHeadError, DepartmentNotFoundError, NoHeadForHeadError, NoHeadForDepartamentFoundError


class Department(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return str(self.name)


class User(AbstractUser):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='users', verbose_name='Отдел',
                                   null=True, blank=True)
    position = models.CharField(max_length=100, verbose_name='Должность')
    photo = models.ImageField(upload_to='static/photos', verbose_name='Фото', null=True, blank=True)
    is_intern = models.BooleanField(default=False, verbose_name='Является стажером')
    is_head = models.BooleanField(default=False, verbose_name='Является руководителем')
    is_awaiting_feedback = models.BooleanField(default=False, verbose_name='Ожидает отзыва')
    feedback_viewed = models.ForeignKey("Feedback", on_delete=models.CASCADE, related_name='feedback_viewed',
                                        verbose_name='Просмотренные отзывы', null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname} <{self.email}>"

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)

    @property
    def slaves_for_head(self) -> QuerySet["User"]:
        if not self.is_head:
            raise IsNotHeadError
        head_department = self.department
        if not head_department:
            raise DepartmentNotFoundError
        slaves_and_head_in_department = self.objects.filter(department=head_department)
        return slaves_and_head_in_department.exclude(pk=self.pk)

    @property
    def reviewers(self) -> QuerySet["User"]:
        if self.is_intern:
            return self._meta.model.objects.filter(pk=self.head_of_employee.pk)  # преобразование instance в queryset
        return self._meta.model.objects.filter(department=self.department).exclude(pk=self.pk)

    @property
    def head_of_employee(self) -> "User":
        if self.is_head:
            raise NoHeadForHeadError
        user_department = self.department
        if not user_department:
            raise DepartmentNotFoundError
        try:
            return self._meta.model.objects.filter(department=user_department).get(is_head=True)
        except User.DoesNotExist:
            raise NoHeadForDepartamentFoundError

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class WaitForReview(models.Model):
    to_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wait_for_review_user',
                                verbose_name='Пользователь, который запросил обратную связь')
    from_users = models.ManyToManyField(User, verbose_name="Пользователи, которые должны дать обратную связь", related_name='wait_for_review_from_users', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = "Ожидание обратной связи"
        verbose_name_plural = "Ожидания обратных связей"


class Feedback(models.Model):
    to_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='feedback_to_user',
                                   verbose_name='Пользователь')
    from_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='feedback_from_user',
                                     verbose_name='Отправитель')
    score = models.IntegerField(verbose_name='Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    score_tone = models.IntegerField(verbose_name='Тональность оценки',
                                     validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        verbose_name = 'Общий отзыв'
        verbose_name_plural = 'Общие отзывы'

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk:
            self.score_tone = 0
            for item in self.feedback_items.all():
                self.score_tone += item.score_tone
            self.score_tone /= len(self.feedback_items.all())
        super().save()


class FeedbackItem(models.Model):
    metric_name = models.CharField(max_length=500, verbose_name='Название метрики')
    text = models.TextField(verbose_name='Текст')
    score_tone = models.IntegerField(verbose_name='Тональность оценки',
                                     validators=[MinValueValidator(-1), MaxValueValidator(1)])
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='feedback_items',
                                 verbose_name='Общий отзыв')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"{self.metric_name} ({self.feedback.from_user} -> {self.feedback.to_user})"
