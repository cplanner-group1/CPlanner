# Generated by Django 3.2 on 2021-05-29 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='index',
            field=models.IntegerField(default=0),
        ),
    ]