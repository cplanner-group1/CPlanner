# Generated by Django 3.2 on 2021-06-12 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('charts', '0007_auto_20210612_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='build_date',
            field=models.DateField(default='2021-06-12'),
        ),
        migrations.AddField(
            model_name='chart',
            name='owner',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chart',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='chart',
            name='used',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='timetable',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
