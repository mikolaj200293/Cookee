import pytest
from django.test import Client
from random import randint, choice, sample
from main_app.utils import three_new_products_create, new_user_create, three_new_persons_create

from main_app.models import Product, ProductCategory, Recipe, Plan

from faker import Faker

faker = Faker("pl_PL")


@pytest.fixture
def client():
    c = Client()
    return c


@pytest.fixture
def new_three_products():
    return list(three_new_products_create())


@pytest.fixture
def new_three_recipes():
    products = list(three_new_products_create())
    recipes_names = ['Spaghetti', 'Twarożek', 'Kanapki']
    for recipe in recipes_names:
        instance = Recipe.objects.create(recipe_name=recipe,
                                         description=f'Sposób przygotowania {recipe}',
                                         preparation_time=randint(0, 120),
                                         portions=randint(0, 4))
        instance.products.set(sample(products, 2))
    return list(Recipe.objects.all())


@pytest.fixture
def new_three_plans():
    plans_names = ['Standard', 'Fit', 'Sport']
    user = new_user_create()
    persons = three_new_persons_create()
    for plan in plans_names:
        instance = Plan.objects.create(plan_name=plan,
                                       user=user,
                                       plan_length=randint(1, 14))
        instance.persons.set(sample(persons, 2))
    return list(Plan.objects.all())


@pytest.fixture
def new_three_persons():
    return three_new_persons_create()
