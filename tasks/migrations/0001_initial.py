# Generated by Django 3.2 on 2021-05-05 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('group', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0)),
                ('deadline', models.DateTimeField()),
                ('priority', models.IntegerField(default=0)),
                ('last_edit', models.DateTimeField()),
                ('description', models.TextField()),
            ],
        ),
    ]