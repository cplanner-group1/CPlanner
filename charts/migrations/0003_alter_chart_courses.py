# Generated by Django 3.2 on 2021-06-09 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0002_auto_20210609_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='courses',
            field=models.TextField(),
        ),
    ]
