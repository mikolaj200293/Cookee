from random import randrange
from django.contrib.auth.models import User
from main_app.models import Recipe, Product, ProductCategory
from main_app.forms import RecipeForm
from main_app.utils import three_new_products_create
from django.contrib.auth import authenticate, login, logout

import pytest
from faker import Faker
from django.urls import reverse
from main_app.models import Persons

faker = Faker('pl_PL')


@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user(client):
    assert User.objects.count() == 0
    post_data = {
        'login': 'Test_user',
        'password': 'Test_password',
        'confirm_password': 'Test_password',
        'first_name': 'Jan',
        'last_name': 'Kowalski',
        'mail': 'jan@wp.pl'
    }
    response = client.post(reverse('add-user'), post_data)
    assert response.status_code == 302
    assert User.objects.count() == 1
    assert User.objects.first().username == post_data['login']


@pytest.mark.django_db
def test_login_view(client):
    assert User.objects.count() == 0
    User.objects.create_user(username='Test_user', password='Test_password')
    assert User.objects.count() == 1
    post_data = {
        'username': 'Test_user',
        'password': 'Test_password'
    }
    response = client.post(reverse('login'), post_data)
    assert response.status_code == 302
    assert authenticate(username='Test_user', password='Test_password')


@pytest.mark.django_db
def test_logout_view(client, new_user):

    assert new_user.is_authenticated
    response = client.get(reverse('logout'))
    assert response.status_code == 200
    assert 'Zaloguj' in str(response.content)


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
def test_add_person(client, new_user):
    assert User.objects.count() == 1
    persons_count = Persons.objects.count()
    assert persons_count == 0
    name = 'Test_person'
    calories = '2000'
    post_data = {
        'name': name,
        'calories': calories
    }
    response = client.post(reverse('add-person'), post_data)
    assert response.status_code == 200
    assert Persons.objects.count() == persons_count + 1
    person = Persons.objects.first()
    assert person.name == name
    assert person.calories == int(calories)


@pytest.mark.django_db
def test_delete_person(client, new_user):
    assert User.objects.count() == 1
    person = Persons.objects.create(name=faker.first_name(), calories=2000, user=new_user)
    assert Persons.objects.count() == 1
    response = client.post(reverse('delete-person', kwargs={'pk': person.pk}))
    assert response.status_code == 302
    assert Persons.objects.count() == 0


@pytest.mark.django_db
def test_person_update(client, new_user):
    assert User.objects.count() == 1
    person = Persons.objects.create(name='Test_person', calories=2000, user=new_user)
    assert Persons.objects.count() == 1
    new_person_name = 'Updated_person_name'
    new_calories = 1500
    post_data = {
        'name': new_person_name,
        'calories': new_calories,
    }
    response = client.post(reverse('edit-person', kwargs={'person_id': person.pk}), post_data)
    assert response.status_code == 302
    assert Persons.objects.last().name == new_person_name


@pytest.mark.django_db
def test_add_recipe(client, new_three_products, new_user):
    assert User.objects.count() == 1
    recipes_count = Recipe.objects.count()
    assert recipes_count == 0
    recipe_name = 'Test_recipe'
    description = 'Test_description'
    preparation_time = 30
    products = Product.objects.all()
    portions = 4.0
    post_data = {
        'recipe_name': recipe_name,
        'description': description,
        'preparation_time': preparation_time,
        'products': (products[1].pk, products[2].pk),
        'portions': portions
    }
    form = RecipeForm(data=post_data)
    assert form.is_valid()
    response = client.post('/add_recipe', data=post_data)
    assert response.status_code == 302
    assert Recipe.objects.count() == recipes_count + 1
    recipe = Recipe.objects.first()
    assert recipe.recipe_name == recipe_name
    assert recipe.description == description
    assert recipe.preparation_time == preparation_time
    n = 1
    for product in recipe.products.all():
        assert product == products[n]
        n += 1


@pytest.mark.django_db
def test_delete_recipe(client, new_three_products, new_user):
    assert User.objects.count() == 1
    recipe = Recipe.objects.create(recipe_name='Test_recipe',
                                   description='Test_description',
                                   preparation_time=10,
                                   portions=4)
    recipe.products.set(Product.objects.all())
    assert Recipe.objects.count() == 1
    response = client.post(reverse('delete-recipe', kwargs={'pk': recipe.pk}))
    assert response.status_code == 302
    assert Recipe.objects.count() == 0


@pytest.mark.django_db
def test_recipe_update(client, new_three_products, new_user):
    assert User.objects.count() == 1
    recipe = Recipe.objects.create(recipe_name='Test_recipe',
                                   description='Test_description',
                                   preparation_time=10,
                                   portions=4)
    recipe.products.set(Product.objects.all())
    assert Recipe.objects.count() == 1
    recipe_name = 'Updated_recipe'
    description = 'Updated_description'
    preparation_time = 30
    products = Product.objects.all()
    portions = 4.00
    post_data = {
        'recipe_name': recipe_name,
        'description': description,
        'preparation_time': preparation_time,
        'products': (products[0].pk, products[1].pk),
        'portions': portions
    }
    response = client.post(reverse('edit-recipe', kwargs={'recipe_id': recipe.pk}), post_data)
    assert response.status_code == 302
    assert Recipe.objects.last().recipe_name == recipe_name


@pytest.mark.django_db
def test_add_product(client, new_user):
    assert User.objects.count() == 1
    category = ProductCategory.objects.create(category_name='Test_category')
    products_count = Product.objects.count()
    post_data = {
        'product_name': 'Test_product',
        'proteins': 10.0,
        'carbohydrates': 15.0,
        'fats': 7.0,
        'category': category.pk
    }
    response = client.post(reverse('add-product'), post_data)
    assert response.status_code == 200
    assert Product.objects.count() == products_count + 1
    product = Product.objects.first()
    assert product.product_name == post_data['product_name']
    assert product.fats == post_data['fats']


@pytest.mark.django_db
def test_delete_product(client, new_user):
    assert User.objects.count() == 1
    category = ProductCategory.objects.create(category_name='Test_category')
    product = Product.objects.create(product_name='Test_product',
                                     proteins=10.0,
                                     carbohydrates=15.0,
                                     fats=7.0,
                                     category=category)
    assert Product.objects.count() == 1
    response = client.post(reverse('delete-product', kwargs={'pk': product.pk}))
    assert response.status_code == 302
    assert Recipe.objects.count() == 0
