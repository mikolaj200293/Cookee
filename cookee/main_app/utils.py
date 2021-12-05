from main_app.models import Product, ProductCategory, Persons
from random import randint, choice, sample, randrange
from django.contrib.auth.models import User

from faker import Faker

faker = Faker("pl_PL")



def three_new_products_create():
    categories_names = ['Nabiał', 'Pieczywo', 'Mięso']
    for category in categories_names:
        ProductCategory.objects.create(category_name=category)
    categories = ProductCategory.objects.all()
    products_names = ['Chleb', 'Ser', 'Mięso mielone']
    for product in products_names:
        Product.objects.create(product_name=product,
                               proteins=randint(0, 100),
                               carbohydrates=randint(0, 100),
                               fats=randint(0, 100),
                               category=choice(categories))
    return Product.objects.all()


def new_user_create():
    user = User.objects.create_user(username=faker.first_name(),
                                    password='test_password',
                                    first_name='user_first_name',
                                    last_name='user_last_name',
                                    email='test@email.com')
    return User.objects.last()


def three_new_persons_create():
    user = new_user_create()
    persons_names = ['Person1', 'Person2', 'Person3']
    for person in persons_names:
        Persons.objects.create(name=person,
                               calories=randrange(1000, 4000, 100),
                               user=user)
    return list(Persons.objects.all())
