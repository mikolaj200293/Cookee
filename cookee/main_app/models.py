from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError

MEALS = (
    (1, 'śniadanie'),
    (2, 'drugie śniadanie'),
    (3, 'obiad'),
    (4, 'podwieczorek'),
    (5, 'kolacja')
)


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.category_name}"


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='Nazwa produktu')
    proteins = models.FloatField(null=True, verbose_name='Białka')
    carbohydrates = models.FloatField(null=True, verbose_name='Węglowodany')
    fats = models.FloatField(null=True, verbose_name='Tłuszcze')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Kategoria')
    add_date = models.DateField(auto_created=True, auto_now=True)

    @property
    def calories(self):
        calories_calculated = self.proteins * 4 + self.carbohydrates * 4 + self.fats * 9
        return calories_calculated

    def __str__(self):
        return f"{self.product_name}"


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    preparation_time = models.IntegerField()
    products = models.ManyToManyField(Product, through='ProductsQuantities')
    portions = models.IntegerField(default=4)
    add_date = models.DateField(auto_created=True, auto_now=True)
    edit_date = models.DateField(auto_now_add=True)

    @property
    def recipe_calories(self):
        calories_calculated = 0
        for product in self.products.all():
            calories_calculated += product.calories
        return calories_calculated

    def __str__(self):
        return f"{self.recipe_name} ({self.recipe_calories} kcal)"


class Persons(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Plan(models.Model):
    plan_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_length = models.IntegerField()
    persons = models.ManyToManyField(Persons)

    def __str__(self):
        return f"{self.plan_name}"


class Meal(models.Model):
    plan_name = models.ManyToManyField(Plan)
    plan_day = models.IntegerField()
    meal = models.IntegerField(choices=MEALS, null=True)
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plan_name}"


class ProductsQuantities(models.Model):
    product_quantity = models.FloatField(default=0)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
