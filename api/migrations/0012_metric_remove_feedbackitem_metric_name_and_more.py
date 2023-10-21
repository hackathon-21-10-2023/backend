# Generated by Django 4.2.6 on 2023-10-21 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_user_should_give_feedback_to_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='feedbackitem',
            name='metric_name',
        ),
        migrations.AddField(
            model_name='feedbackitem',
            name='metric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.metric'),
        ),
    ]
