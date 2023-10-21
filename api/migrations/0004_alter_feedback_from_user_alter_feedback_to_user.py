# Generated by Django 4.2.6 on 2023-10-21 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_feedback_from_user_alter_feedback_to_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='from_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_from_user', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='to_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_to_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]