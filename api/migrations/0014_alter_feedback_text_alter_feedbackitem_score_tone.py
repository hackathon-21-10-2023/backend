# Generated by Django 4.2.6 on 2023-10-22 09:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0013_alter_metric_options_feedbackitem_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="text",
            field=models.TextField(blank=True, null=True, verbose_name="Текст"),
        ),
        migrations.AlterField(
            model_name="feedbackitem",
            name="score_tone",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(-1),
                    django.core.validators.MaxValueValidator(1),
                ],
                verbose_name="Тональность оценки",
            ),
        ),
    ]