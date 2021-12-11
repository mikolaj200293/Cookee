from django.db import models
from django.contrib.auth.models import User


MEALS = (
    (1, 'śniadanie'),
    (2, 'drugie śniadanie'),
    (3, 'obiad'),
    (4, 'podwieczorek'),
    (5, 'kolacja')
)


class ProductCategory(models.Model):
    """
    Product Category model.
    """
    category_name = models.CharField(max_length=100, unique=True, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.category_name}"


class Product(models.Model):
    """
    Product model.
    """
    product_name = models.CharField(max_length=100, verbose_name='Nazwa produktu')
    proteins = models.DecimalField(null=True, verbose_name='Białka', decimal_places=2, max_digits=6)
    carbohydrates = models.DecimalField(null=True, verbose_name='Węglowodany', decimal_places=2, max_digits=6)
    fats = models.DecimalField(null=True, verbose_name='Tłuszcze', decimal_places=2, max_digits=6)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Kategoria')
    add_date = models.DateField(auto_created=True, auto_now=True)

    @property
    def calories(self):
        """
        Calculate product calories.
        """
        calories_calculated = self.proteins * 4 + self.carbohydrates * 4 + self.fats * 9
        return round(calories_calculated, 2)

    def __str__(self):
        return f"{self.product_name}"


class Recipe(models.Model):
    """
    Recipe model.
    """
    recipe_name = models.CharField(max_length=100, unique=True, verbose_name='Nazwa przepisu')
    description = models.TextField(verbose_name='Opis przygotowania')
    preparation_time = models.IntegerField(verbose_name='Czas przygotowania')
    products = models.ManyToManyField(Product, through='ProductsQuantities', verbose_name='Produkty')
    portions = models.DecimalField(default=4, verbose_name='Porcje', decimal_places=1, max_digits=3)
    add_date = models.DateField(auto_created=True, auto_now=True)
    edit_date = models.DateField(auto_now_add=True)

    @property
    def recipe_calories(self):
        """
        Calculate recipe calories.
        """
        calories_calculated = 0
        for product in self.products.all():
            calories_calculated += product.calories * product.productsquantities_set.\
                get(product_id=product.id, recipe_id=self.pk).product_quantity / 100
        return round(calories_calculated, 2)

    @property
    def portion_calories(self):
        """
        Calculate 1 portion of recipe meal calories.
        """
        return round(self.recipe_calories / self.portions, 2)

    def __str__(self):
        return f"{self.recipe_name}"


class Persons(models.Model):
    """
    Persons model.
    """
    name = models.CharField(max_length=100, verbose_name='Imię')
    calories = models.IntegerField(verbose_name='Zapotrzebowanie na kalorie')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Plan(models.Model):
    """
    Plan model.
    """
    plan_name = models.CharField(max_length=100, verbose_name='Nazwa planu')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_length = models.IntegerField(verbose_name='Długość planu')
    persons = models.ManyToManyField(Persons, verbose_name='Osoby')
    date_modified = models.DateTimeField(auto_now=True)

    @property
    def plan_calories(self):
        """
        Calculate plan calories to cover by meals.
        """
        result = 0
        for person in self.persons.all():
            result += person.calories
        return result

    def __str__(self):
        return f"{self.plan_name}"


class Meal(models.Model):
    """
    Meal model.
    """
    plan_name = models.ManyToManyField(Plan, verbose_name='Nazwa planu')
    plan_day = models.IntegerField(verbose_name='Dzień planu')
    meal = models.IntegerField(choices=MEALS, null=True, verbose_name='Posiłek')
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Przepis')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_portions = models.DecimalField(verbose_name='Porcje', decimal_places=1, max_digits=3)
    date_modified = models.DateTimeField(auto_now=True)

    @property
    def meal_calories(self):
        """
        Calculate meal calories.
        """
        result = self.recipes.portion_calories * self.meal_portions
        return result

    def __str__(self):
        return f"{self.plan_name}"


class ProductsQuantities(models.Model):
    """
    Products quantities model.
    """
    product_quantity = models.DecimalField(default=0, verbose_name='Ilość produktu', decimal_places=1, max_digits=8)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def one_portion_product_quantity(self):
        """
        Calculate quantity of product in one portion of related recipe.
        """
        result = self.product_quantity / self.recipe_id.portions
        return result


class ShoppingList(models.Model):
    """
    Shopping list model.
    """
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ShoppingListProducts')
    date_created = models.DateTimeField(auto_created=True, auto_now=True)
    name = models.CharField(max_length=100)


class ShoppingListProducts(models.Model):
    """
    Shopping list products model.
    """
    product_quantity = models.DecimalField(default=0, decimal_places=1, max_digits=8)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)