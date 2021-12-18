import pytest
from django.test import Client
from random import randint, sample
from main_app.utils import three_new_products_create, new_user_create, three_new_persons_create

from main_app.models import Recipe, Plan

from django.contrib.auth.models import User

from faker import Faker

faker = Faker("pl_PL")


@pytest.fixture
def client():
    """
    Create Client() object
    """
    c = Client()
    return c


@pytest.fixture
def new_three_products():
    """
    Create list of 3 Product model objects
    """
    return list(three_new_products_create())


@pytest.fixture
def new_three_recipes():
    """
    Create list of 3 Recipe model objects
    """
    products = list(three_new_products_create())
    recipes_names = ['Spaghetti', 'Twarożek', 'Kanapki']
    for recipe in recipes_names:
        instance = Recipe.objects.create(recipe_name=recipe,
                                         description=f'Sposób przygotowania {recipe}',
                                         preparation_time=randint(0, 120),
                                         portions=randint(100, 400)/100)
        instance.products.set(sample(products, 2))
    recipes = Recipe.objects.all()
    for recipe in recipes:
        for product in recipe.productsquantities_set.all():
            product.product_quantity = randint(100, 1000)
            product.save()
    return list(Recipe.objects.all())


@pytest.fixture
def new_three_plans():
    """
    Create list of 3 Plan model objects
    """
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
    """
    Create list of 3 Plan model objects
    """
    return three_new_persons_create()


@pytest.fixture
def new_user_login(client):
    """
    Create new User model object and logs created user in.
    :param client: Django Client() object.
    :return: Created user object.
    """
    user = User.objects.create_user(username=faker.first_name(), password='12345')
    client.force_login(user)
    return user


