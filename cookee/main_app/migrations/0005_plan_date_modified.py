# Generated by Django 3.2.9 on 2021-11-27 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_meal_date_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]