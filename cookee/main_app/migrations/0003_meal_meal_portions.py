# Generated by Django 3.2.9 on 2021-11-27 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20211122_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='meal_portions',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]