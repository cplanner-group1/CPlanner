# Generated by Django 3.2 on 2021-06-11 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0004_auto_20210609_1242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursetracker',
            name='prerequisites',
        ),
    ]