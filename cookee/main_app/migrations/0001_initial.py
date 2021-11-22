# Generated by Django 3.2.9 on 2021-11-21 20:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('calories', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_created=True, auto_now=True)),
                ('product_name', models.CharField(max_length=100)),
                ('proteins', models.FloatField(null=True)),
                ('carbohydrates', models.FloatField(null=True)),
                ('fats', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductsQuantities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.FloatField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_created=True, auto_now=True)),
                ('recipe_name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('preparation_time', models.IntegerField()),
                ('portions', models.IntegerField(default=4)),
                ('edit_date', models.DateField(auto_now_add=True)),
                ('products', models.ManyToManyField(through='main_app.ProductsQuantities', to='main_app.Product')),
            ],
        ),
        migrations.AddField(
            model_name='productsquantities',
            name='recipe_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.recipe'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.productcategory'),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100)),
                ('plan_length', models.IntegerField()),
                ('persons', models.ManyToManyField(to='main_app.Persons')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_day', models.IntegerField()),
                ('meal', models.IntegerField(choices=[(1, 'śniadanie'), (2, 'drugie śniadanie'), (3, 'obiad'), (4, 'podwieczorek'), (5, 'kolacja')], null=True)),
                ('plan_name', models.ManyToManyField(to='main_app.Plan')),
                ('recipes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]