# Generated by Django 3.2 on 2021-06-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0013_auto_20210615_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='build_date',
            field=models.DateField(default='2021-06-16'),
        ),
        migrations.AlterField(
            model_name='semestercourse',
            name='priority',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='semestercourse',
            name='selected',
            field=models.IntegerField(default=0),
        ),
    ]
