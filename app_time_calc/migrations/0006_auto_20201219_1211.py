# Generated by Django 3.1.4 on 2020-12-19 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_time_calc', '0005_remove_timeentry_time_worked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeentry',
            name='time_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='time_rest',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='time_start',
            field=models.DateTimeField(),
        ),
    ]
