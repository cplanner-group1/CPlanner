# Generated by Django 3.2 on 2021-06-14 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0011_alter_course_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursetracker',
            name='prerequisites',
            field=models.TextField(default=''),
        ),
    ]
