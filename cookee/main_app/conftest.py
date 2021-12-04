import pytest
from django.test import Client
from random import randint, choice

from main_app.models import Product, ProductCategory


from faker import Faker
faker = Faker("pl_PL")



@pytest.fixture
def client():
    c = Client()
    return c


@pytest.fixture
def new_three_products():
    categories_names = ['Nabiał', 'Pieczywo', 'Mięso']
    for category in categories_names:
        ProductCategory.objects.create(category_name=category)
    categories = ProductCategory.objects.all()
    products_names = ['Chleb', 'Ser', 'Mięso mielone']
    for product in products_names:
        Product.objects.create(product_name=product, proteins=randint(0, 100), carbohydrates=randint(0, 100),
                               fats=randint(0, 100), category=choice(categories))
    return list(Product.objects.all())


@pytest.fixture
def new_three_recipes():
    categories_names = ['Nabiał', 'Pieczywo', 'Mięso']
    for category in categories_names:
        ProductCategory.objects.create(category_name=category)
    categories = ProductCategory.objects.all()
    products_names = ['Chleb', 'Ser', 'Mięso mielone']
    for product in products_names:
        Product.objects.create(product_name=product, proteins=randint(0, 100), carbohydrates=randint(0, 100),
                               fats=randint(0, 100), category=choice(categories))
    return list(Product.objects.all())
