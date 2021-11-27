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
        return round(calories_calculated, 2)

    def __str__(self):
        return f"{self.product_name}"


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100, unique=True, verbose_name='Nazwa przepisu')
    description = models.TextField(verbose_name='Opis przygotowania')
    preparation_time = models.IntegerField(verbose_name='Czas przygotowania')
    products = models.ManyToManyField(Product, through='ProductsQuantities', verbose_name='Produkty')
    portions = models.IntegerField(default=4, verbose_name='Porcje')
    add_date = models.DateField(auto_created=True, auto_now=True)
    edit_date = models.DateField(auto_now_add=True)

    @property
    def recipe_calories(self):
        calories_calculated = 0
        for product in self.products.all():
            calories_calculated += product.calories * product.productsquantities_set.get(product_id=product.id).\
                product_quantity / 100
        return round(calories_calculated, 2)

    @property
    def portion_calories(self):
        return round(self.recipe_calories / self.portions, 2)

    def __str__(self):
        return f"{self.recipe_name} (4 porcje: {self.recipe_calories} kcal)"


class Persons(models.Model):
    name = models.CharField(max_length=100, verbose_name='Imię')
    calories = models.IntegerField(verbose_name='Zapotrzebowanie na kalorie')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Plan(models.Model):
    plan_name = models.CharField(max_length=100, verbose_name='Nazwa planu')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_length = models.IntegerField(verbose_name='Długość planu')
    persons = models.ManyToManyField(Persons, verbose_name='Osoby')
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan_name}"


class Meal(models.Model):
    plan_name = models.ManyToManyField(Plan, verbose_name='Nazwa planu')
    plan_day = models.IntegerField(verbose_name='Dzień planu')
    meal = models.IntegerField(choices=MEALS, null=True, verbose_name='Posiłek')
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Przepis')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_portions = models.IntegerField(verbose_name='Porcje')
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan_name}"


class ProductsQuantities(models.Model):
    product_quantity = models.FloatField(default=0, verbose_name='Ilość produktu')
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def one_portion_product_quantity(self):
        result = self.product_quantity / self.recipe_id.portions
        return result
