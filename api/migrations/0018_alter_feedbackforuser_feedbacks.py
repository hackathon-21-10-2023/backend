# Generated by Django 4.2.6 on 2023-10-22 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0017_remove_feedback_created_at_feedbackforuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedbackforuser",
            name="feedbacks",
            field=models.ManyToManyField(
                blank=True,
                related_name="feedbacks_for_user",
                to="api.feedback",
                verbose_name="Отзыв об одном сотруднике",
            ),
        ),
    ]