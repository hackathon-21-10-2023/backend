# Generated by Django 4.2.6 on 2023-10-22 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_metric_remove_feedbackitem_metric_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metric',
            options={'verbose_name': 'Метрика', 'verbose_name_plural': 'Метрики'},
        ),
        migrations.AddField(
            model_name='feedbackitem',
            name='score',
            field=models.IntegerField(default=5, verbose_name='Оценка'),
        ),
    ]