# Generated by Django 3.1.4 on 2020-12-19 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_time_calc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dummy',
            name='last_name',
            field=models.CharField(default='Doe', max_length=50),
            preserve_default=False,
        ),
    ]
