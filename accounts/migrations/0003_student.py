# Generated by Django 3.2 on 2021-05-29 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210509_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('university', models.CharField(default='', max_length=100)),
                ('field', models.CharField(default='', max_length=100)),
                ('entry_year', models.IntegerField()),
                ('gpa', models.FloatField()),
                ('taken_units', models.IntegerField()),
                ('passed_units', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
