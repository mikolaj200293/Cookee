# Generated by Django 3.2.9 on 2021-11-30 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20211130_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main_app.plan'),
            preserve_default=False,
        ),
    ]