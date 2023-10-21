from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class User(AbstractBaseUser):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    password = models.CharField(max_length=100, verbose_name='Пароль')
    email = models.EmailField(unique=True, verbose_name='Email')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='users', verbose_name='Отдел')
    position = models.CharField(max_length=100, verbose_name='Должность')
    photo = models.ImageField(upload_to='photos', verbose_name='Фото')
    is_intern = models.BooleanField(default=False, verbose_name='Является стажером')
    is_head = models.BooleanField(default=False, verbose_name='Является руководителем')
    is_awaiting_feedback = models.BooleanField(default=False, verbose_name='Ожидает отзыва')

    def __str__(self):
        return f"{self.name} {self.surname} <{self.email}>"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
