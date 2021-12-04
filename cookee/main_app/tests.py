import pytest
from faker import Faker
from django.urls import reverse
from main_app.models import Product
faker = Faker('pl_PL')


@pytest.mark.django_db
def test_products_view(client, new_three_products):
    response = client.get('/products')
    assert response.status_code == 200
    products = response.context['products']
    assert list(products) == new_three_products


@pytest.mark.django_db
def test_recipes_view(client, new_three_recipes):
    response = client.get('/products')
    assert response.status_code == 200
    products = response.context['products']
    assert list(products) == new_three_products
