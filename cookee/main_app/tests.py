from random import randrange
from django.contrib.auth.models import User
from main_app.models import Recipe, Product
from main_app.utils import three_new_products_create

import pytest
from faker import Faker
from django.urls import reverse
from main_app.models import Persons
faker = Faker('pl_PL')


@pytest.mark.django_db
def test_products_view(client, new_three_products):
    response = client.get('/products')
    assert response.status_code == 200
    products = response.context['products']
    assert list(products) == new_three_products


@pytest.mark.django_db
def test_recipes_view(client, new_three_recipes):
    response = client.get('/recipes')
    assert response.status_code == 200
    recipes = response.context['recipes']
    assert list(recipes) == new_three_recipes


@pytest.mark.django_db
def test_plans_view(client, new_three_plans):
    response = client.get('/plans')
    assert response.status_code == 200
    plans = response.context['plans']
    assert list(plans) == new_three_plans


@pytest.mark.django_db
def test_persons_view(client, new_three_persons):
    response = client.get('/persons')
    assert response.status_code == 200
    persons = response.context['persons']
    assert list(persons) == new_three_persons


@pytest.mark.django_db
def test_add_person(client):
    assert User.objects.count() == 0
    user = User.objects.create_user(username=faker.first_name(), password='12345')
    assert User.objects.count() == 1
    client.login(username=user.username, password=user.password)
    persons_count = Persons.objects.count()
    assert persons_count == 0
    name = 'Test_person'
    calories = '2000'
    post_data = {
        'name': name,
        'calories': calories
    }
    response = client.post(reverse('add-person'), post_data)
    assert response.status_code == 302
    assert Persons.objects.count() == persons_count + 1
    person = Persons.objects.first()
    assert person.name == name
    assert person.calories == int(calories)


@pytest.mark.django_db
def test_add_recipe(client, new_three_products):
    assert User.objects.count() == 0
    user = User.objects.create_user(username=faker.first_name(), password='12345')
    assert User.objects.count() == 1
    client.login(username=user.username, password=user.password)
    client.request()
    recipes_count = Recipe.objects.count()
    assert recipes_count == 0
    recipe_name = 'Test_recipe'
    description = 'Test_description'
    preparation_time = '30'
    products = Product.objects.all()
    portions = '4'
    post_data = {
        'recipe_name': recipe_name,
        'description': description,
        'preparation_time': preparation_time,
        'products': products,
        'portions': portions
    }
    response = client.post(reverse('add-recipe'), post_data)
    assert response.status_code == 302
    assert Recipe.objects.count() == recipes_count + 1
    recipe = Recipe.objects.first()
    assert recipe.recipe_name == recipe_name
    assert recipe.description == description
    assert recipe.preparation_time == preparation_time
    assert recipe.products == products
