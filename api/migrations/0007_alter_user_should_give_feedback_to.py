# Generated by Django 4.2.6 on 2023-10-21 20:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_user_should_give_feedback_to"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="should_give_feedback_to",
            field=models.ManyToManyField(
                to=settings.AUTH_USER_MODEL,
                verbose_name="Должен дать обратную связь следующим людям",
            ),
        ),
    ]
