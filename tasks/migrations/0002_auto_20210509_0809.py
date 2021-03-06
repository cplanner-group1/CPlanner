# Generated by Django 3.2 on 2021-05-09 08:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='last_edit',
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='group',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
