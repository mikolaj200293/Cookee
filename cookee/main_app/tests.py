from random import randint, sample
from django.contrib.auth.models import User

from main_app.functions import calculate_days_calories
from main_app.models import Recipe, Product, ProductCategory, Plan, Meal, ProductsQuantities, ShoppingList, \
    ShoppingListProducts
from main_app.forms import RecipeForm
from django.contrib.auth import authenticate
from main_app.utils import three_new_persons_create

import pytest
from faker import Faker
from django.urls import reverse
from main_app.models import Persons

faker = Faker('pl_PL')


@pytest.mark.django_db
def test_home_view(client):
    """
    Test HomeView view.
    :param client: Django Client() object.
    :return: Assert response status code.
    """
    response = client.get(reverse('home'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user(client):
    """
    Test AddUserView view.
    :param client: Django Client() object.
    :return: Assert if User model object is correctly created.
    """
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
    """
    Test LoginView view.
    :param client: Django Client() object.
    :return: Asser if user is correctly logged-in and view redirects to next url.
    """
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
def test_logout_view(client, new_user_login):
    """
    Test LogoutView view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if view stays the same url and if 'Zaloguj' shows on the website.
    """
    assert new_user_login.is_authenticated
    response = client.get(reverse('logout'))
    assert response.status_code == 200
    assert 'Zaloguj' in str(response.content)


@pytest.mark.django_db
def test_products_view(client, new_three_products):
    """
    Test ProductsView view.
    :param client: Django Client() object.
    :param new_three_products: Fixture that creates 3 Product model objects
    :return: Assert if all created products shows on the website
    """
    response = client.get('/products')
    assert response.status_code == 200
    products = response.context['products']
    assert list(products) == new_three_products


@pytest.mark.django_db
def test_recipes_view(client, new_three_recipes):
    """
    Test RecipesView view.
    :param client: Django Client() object.
    :param new_three_recipes: Fixture that creates 3 Recipe model objects
    :return: Assert if all created recipes shows on the website
    """
    response = client.get('/recipes')
    assert response.status_code == 200
    recipes = response.context['recipes']
    assert list(recipes) == new_three_recipes


@pytest.mark.django_db
def test_plans_view(client, new_three_plans):
    """
    Test PlansView view.
    :param client: Django Client() object.
    :param new_three_plans: Fixture that creates 3 Plan model objects
    :return: Assert if all created plans shows on the website
    """
    response = client.get('/plans')
    assert response.status_code == 200
    plans = response.context['plans']
    assert list(plans) == new_three_plans


@pytest.mark.django_db
def test_persons_view(client, new_three_persons):
    """
    Test PersonsView view.
    :param client: Django Client() object.
    :param new_three_persons: Fixture that creates 3 Persons model objects
    :return: Assert if all created persons shows on the website
    """
    response = client.get('/persons')
    assert response.status_code == 200
    persons = response.context['persons']
    assert list(persons) == new_three_persons


@pytest.mark.django_db
def test_add_person(client, new_user_login):
    """
    Test PersonCreate view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Persons model object is correctly created.
    """
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
def test_delete_person(client, new_user_login):
    """
    Test PersonDelete view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Person model object is correctly deleted.
    """
    assert User.objects.count() == 1
    person = Persons.objects.create(name=faker.first_name(), calories=2000, user=new_user_login)
    assert Persons.objects.count() == 1
    response = client.post(reverse('delete-person', kwargs={'pk': person.pk}))
    assert response.status_code == 302
    assert Persons.objects.count() == 0


@pytest.mark.django_db
def test_person_update(client, new_user_login):
    """
    Test PersonUpdate view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Person model object is correctly updated.
    """
    assert User.objects.count() == 1
    person = Persons.objects.create(name='Test_person', calories=2000, user=new_user_login)
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
def test_add_recipe(client, new_three_products, new_user_login):
    """
    Test RecipeCreate view.
    :param client: Django Client() object.
    :param new_three_products: Fixture that creates 3 Product model objects.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Recipe model object is correctly created
    """
    assert User.objects.count() == 1
    recipes_count = Recipe.objects.count()
    assert recipes_count == 0
    recipe_name = 'Test_recipe'
    description = 'Test_description'
    preparation_time = 30
    products = Product.objects.all()[0:2]
    portions = 4.0
    post_data = {
        'recipe_name': recipe_name,
        'description': description,
        'preparation_time': preparation_time,
        'products': (products[0].pk, products[1].pk),
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
    for i, product in enumerate(list(recipe.products.all())):
        assert product == products[i]


@pytest.mark.django_db
def test_delete_recipe(client, new_three_products, new_user_login):
    """
    Test RecipeDelete view.
    :param client: Django Client() object.
    :param new_three_products: Fixture that creates 3 Product model objects.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Recipe model object is correctly deleted.
    """
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
def test_recipe_update(client, new_three_products, new_user_login):
    """
    Test RecipeUpdate view.
    :param client: Django Client() object.
    :param new_three_products: Fixture that creates 3 Product model objects.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Recipe model object is correctly updated.
    """
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
def test_add_product(client, new_user_login):
    """
    Test ProductCreate view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Product model object is correctly created.
    """
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
def test_delete_product(client, new_user_login):
    """
    Test ProductDelete view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Product model object is correctly deleted.
    """
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


@pytest.mark.django_db
def test_product_update(client, new_user_login):
    """
    Test ProductUpdate view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Product model object is correctly updated.
    """
    assert User.objects.count() == 1
    category = ProductCategory.objects.create(category_name='Test_category')
    product = Product.objects.create(product_name='Test_product',
                                     proteins=10.0,
                                     carbohydrates=15.0,
                                     fats=7.0,
                                     category=category)
    assert Product.objects.count() == 1
    new_category = ProductCategory.objects.create(category_name='New_category')
    post_data = {
        'product_name': 'Updated_product_name',
        'proteins': 20.0,
        'carbohydrates': 10.0,
        'fats': 20.0,
        'category': new_category.pk
    }
    response = client.post(reverse('edit-product', kwargs={'product_id': product.pk}), post_data)
    assert response.status_code == 302
    assert Product.objects.last().product_name == post_data['product_name']
    assert Product.objects.last().carbohydrates == post_data['carbohydrates']
    assert Product.objects.last().category == new_category


@pytest.mark.django_db
def test_add_plan(client, new_three_persons):
    """
    Test PlanCreate view.
    :param client: Django Client() object.
    :param new_three_persons: Fixture that creates 3 Persons model objects
    :return: Assert if Plan model object is correctly created.
    """
    user = Persons.objects.last().user
    client.force_login(user=user)
    assert User.objects.count() == 1
    plans_count = Plan.objects.count()
    assert plans_count == 0
    persons = Persons.objects.all()[0:2]
    post_data = {
        'plan_name': 'Test_plan',
        'plan_length': randint(1, 21),
        'persons': (persons[0].pk, persons[1].pk)
    }
    response = client.post(reverse('add-plan'), post_data)
    assert response.status_code == 200
    assert Plan.objects.count() == plans_count + 1
    new_plan = Plan.objects.first()
    assert new_plan.plan_name == post_data['plan_name']
    assert new_plan.plan_length == post_data['plan_length']
    for i, person in enumerate(new_plan.persons.all()):
        assert person.name == persons[i].name
    assert new_plan.user == user


@pytest.mark.django_db
def test_delete_plan(client, new_user_login):
    """
    Test PlanDelete view.
    :param client: Django Client() object.
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if Plan model object is correctly deleted.
    """
    assert User.objects.count() == 1
    assert Plan.objects.count() == 0
    persons = three_new_persons_create()
    plan = Plan.objects.create(plan_name='Test_plan',
                               plan_length=randint(1, 21),
                               user=User.objects.first())
    plan.persons.set(persons[0:2])
    assert Plan.objects.count() == 1
    response = client.post(reverse('delete-plan', kwargs={'pk': plan.pk}))
    assert response.status_code == 302
    assert Plan.objects.count() == 0


@pytest.mark.django_db
def test_plan_update(client, new_three_persons):
    """
    Test PlanUpdate view.
    :param client: Django Client() object.
    :param new_three_persons: Fixture that creates 3 Persons model objects
    :return: Assert if Plan model object is correctly updated.
    """
    user = Persons.objects.last().user
    client.force_login(user=user)
    assert User.objects.count() == 1
    plan = Plan.objects.create(plan_name='Test_plan',
                               plan_length=randint(1, 21),
                               user=User.objects.first())
    assert Plan.objects.count() == 1
    persons = Persons.objects.all()[0:2]
    post_data = {
        'plan_name': 'Updated_plan_name',
        'plan_length': randint(1, 21),
        'persons': (persons[0].pk, persons[1].pk)
    }
    response = client.post(reverse('edit-plan', kwargs={'plan_id': plan.pk}), post_data)
    assert response.status_code == 302
    assert Plan.objects.last().plan_name == post_data['plan_name']
    assert Plan.objects.last().plan_length == post_data['plan_length']
    for i, person in enumerate(Plan.objects.last().persons.all()):
        assert person.name == persons[i].name


@pytest.mark.django_db
def test_plan_details_view(client, new_three_plans, new_three_recipes):
    """
    Test PlanDetailsView view.
    :param client: Django Client() object.
    :param new_three_plans: Fixture that creates 3 Plans model objects
    :param new_three_recipes: Fixture that creates 3 Recipes model objects
    :return: Assert if Meal model objects are correctly created or updated.
    """
    user = Persons.objects.last().user
    client.force_login(user=user)
    plans_count = Plan.objects.count()
    assert Persons.objects.count() == 3
    assert plans_count == 3
    assert Recipe.objects.count() == 3
    plan = Plan.objects.last()
    recipes = Recipe.objects.all()
    recipes_primary_keys = [recipe.pk for recipe in recipes]
    for day in range(10):
        meal = Meal.objects.create(plan_day=randint(1, plan.plan_length),
                                   meal=randint(1, 5),
                                   user=user,
                                   meal_portions=randint(100, 1000) / 100,
                                   recipes=Recipe.objects.get(pk=sample(recipes_primary_keys, 1)[0]))
        meal.plan_name.add(plan.pk)
    assert Meal.objects.count() == 10
    days_calories_list = calculate_days_calories(plan)
    get_response = client.get(reverse('plan-details', kwargs={'plan_id': plan.pk}))
    assert get_response.status_code == 200
    context_plan = get_response.context['plan']
    context_persons = get_response.context['persons']
    context_meals = get_response.context['meals']
    context_plan_days = get_response.context['plan_days']
    context_days_calories = get_response.context['days_calories']
    assert context_plan == plan
    assert list(context_persons) == list(plan.persons.all())
    assert list(context_meals) == list(plan.meal_set.all())
    assert context_plan_days == [day for day in range(1, plan.plan_length + 1)]
    assert context_days_calories == days_calories_list

    post_recipe = Recipe.objects.get(pk=sample(recipes_primary_keys, 1)[0])
    post_data = {
        'plan_day': randint(1, plan.plan_length),
        'meal': randint(1, 5),
        'recipes': post_recipe.pk,
        'meal_portions': 12
    }
    post_response = client.post(reverse('plan-details', kwargs={'plan_id': plan.pk}), post_data)
    assert post_response.status_code == 200
    meal_object = Meal.objects.filter(user=user,
                                      plan_name=plan,
                                      plan_day=post_data['plan_day'],
                                      meal=post_data['meal'])
    if Meal.objects.count() == plans_count or Meal.objects.count() == plans_count + 1:
        assert meal_object[0].recipes == post_recipe
        assert meal_object[0].plan_day == post_data['plan_day']
        assert meal_object[0].meal == post_data['meal']
        assert meal_object[0].meal_portions == post_data['meal_portions']
    elif Meal.objects.count() == plans_count and post_response.context['message']:
        assert post_response.context['message'] == 'Przekroczono limit kalorii'
    elif Meal.objects.count() == plans_count + 1 and post_response.context['message']:
        assert post_response.context['message'] == 'Przekroczono limit kalorii'


@pytest.mark.django_db
def test_delete_meal(client, new_three_plans, new_three_recipes):
    """
    Test MealDelete view.
    :param client: Django Client() object.
    :param new_three_plans: Fixture that creates 3 Plans model objects
    :param new_three_recipes: Fixture that creates 3 Recipes model objects
    :return: Assert if Meal model objects are correctly deleted.
    """
    user = Persons.objects.last().user
    client.force_login(user=user)
    plan = Plan.objects.last()
    assert Meal.objects.count() == 0
    meal = Meal.objects.create(plan_day=randint(1, plan.plan_length),
                               meal=randint(1, 5),
                               user=user,
                               meal_portions=randint(100, 1000) / 100,
                               recipes=Recipe.objects.last())
    meal.plan_name.add(plan.pk)
    assert Meal.objects.count() == 1
    response = client.post(reverse('delete-meal', kwargs={'pk': meal.pk}))
    assert response.status_code == 302
    assert Meal.objects.count() == 0


@pytest.mark.django_db
def test_recipe_details_view(client, new_three_recipes, new_user_login):
    """
    Test RecipeDetails View.
    :param client: Django Client() object.
    :param new_three_recipes: Fixture that creates 3 Recipes model objects
    :param new_user_login: Fixture that creates and logs in new user.
    :return: Assert if ProductQuantities model objects are correctly updated.
    """
    assert User.objects.count() == 1
    assert Recipe.objects.count() == 3
    recipe = Recipe.objects.last()
    get_response = client.get(reverse('recipe-details', kwargs={'recipe_id': recipe.pk}))
    assert get_response.status_code == 200
    assert get_response.context['recipe'] == recipe
    assert list(get_response.context['products']) == list(recipe.productsquantities_set.all())

    products = recipe.products.all()
    products_primary_keys = [product.pk for product in products]
    post_data = {
        'product_id': Product.objects.get(pk=sample(products_primary_keys, 1)[0]).pk,
        'product_quantity': randint(1, 1000)
    }
    post_response = client.post(reverse('recipe-details', kwargs={'recipe_id': recipe.pk}), post_data)
    assert post_response.status_code == 200
    product_quantities = ProductsQuantities.objects.filter(recipe_id=recipe, product_id=post_data['product_id'])
    assert product_quantities[0].product_quantity == post_data['product_quantity']


@pytest.mark.django_db
def test_add_shopping_list(client, new_three_plans, new_three_recipes):
    """
    Test ShoppingListCreate view.
    :param client: Django Client() object.
    :param new_three_plans: Fixture that creates 3 Plans model objects
    :param new_three_recipes: Fixture that creates 3 Recipes model objects
    :return: Assert if ShoppingList and ShoppingListProducts models objects are correctly created or updated.
    """
    user = Persons.objects.last().user
    client.force_login(user=user)
    plans_count = Plan.objects.count()
    assert Persons.objects.count() == 3
    assert plans_count == 3
    assert Recipe.objects.count() == 3
    plan = Plan.objects.last()
    recipes = Recipe.objects.all()
    recipes_primary_keys = [recipe.pk for recipe in recipes]
    for day in range(10):
        meal = Meal.objects.create(plan_day=randint(1, plan.plan_length),
                                   meal=randint(1, 5),
                                   user=user,
                                   meal_portions=randint(100, 1000) / 100,
                                   recipes=Recipe.objects.get(pk=sample(recipes_primary_keys, 1)[0]))
        meal.plan_name.add(plan.pk)
    assert Meal.objects.count() == 10
    shopping_list_count = ShoppingList.objects.count()
    assert shopping_list_count == 0
    response = client.get(reverse('shopping-list', kwargs={'plan_id': plan.pk}))
    assert response.status_code == 200
    assert ShoppingList.objects.count() == shopping_list_count + 1
    assert ShoppingListProducts.objects.filter(shopping_list=ShoppingList.objects.first()).count() > 0
    total_plan_products_quantity = 0
    for meal in plan.meal_set.all():
        for product in meal.recipes.productsquantities_set.all():
            total_plan_products_quantity += product.one_portion_product_quantity * meal.meal_portions
    total_shopping_list_products_quantity = 0
    for product in ShoppingListProducts.objects.filter(shopping_list=ShoppingList.objects.first()):
        total_shopping_list_products_quantity += product.product_quantity
    assert round(total_plan_products_quantity, 0) == round(total_shopping_list_products_quantity, 0)


@pytest.mark.django_db
def test_shopping_list_pdf(client, new_three_plans, new_three_recipes):
    """
    Test ShoppingListPdf view.
    :param client: Django Client() object.
    :param new_three_plans: Fixture that creates 3 Plans model objects
    :param new_three_recipes: Fixture that creates 3 Recipes model objects
    :return: Assert if ShoppingListProducts model objects are saved to pdf.
    """
    user = Persons.objects.last().user
    client.force_login(user=user)
    shopping_list = ShoppingList.objects.create(plan=Plan.objects.last())
    products = Product.objects.all()
    for product in products:
        ShoppingListProducts.objects.create(product_quantity=randint(100, 1000),
                                            shopping_list=shopping_list,
                                            product=product)
    response = client.get(reverse('shopping-list-pdf'))
    # print(list(response.streaming_content)[0].decode('UTF-8'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_day_calories_completion(client, new_three_plans, new_three_recipes):
    """
    Test PlanDayCaloriesCompletion view.
    :param client: Django Client() object.
    :param new_three_plans: Fixture that creates 3 Plans model objects
    :param new_three_recipes: Fixture that creates 3 Recipes model objects
    :return: Assert if updated Meal object portions are changing.
    """
    user = Persons.objects.last().user
    client.force_login(user=user)
    plan = Plan.objects.last()
    recipes = Recipe.objects.all()
    recipes_primary_keys = [recipe.pk for recipe in recipes]
    for day in range(10):
        meal_instance = Meal.objects.create(plan_day=randint(1, plan.plan_length),
                                            meal=randint(1, 5),
                                            user=user,
                                            meal_portions=randint(100, 1000) / 100,
                                            recipes=Recipe.objects.get(pk=sample(recipes_primary_keys, 1)[0]))
        meal_instance.plan_name.add(plan.pk)
    meals = Meal.objects.all()
    meal = sample(list(meals), 1)[0]
    plan_day = meal.plan_day
    day_meal = meal.meal
    response = client.get(reverse('fill-calories', kwargs={'plan_id': plan.pk, 'plan_day': plan_day, 'day_meal': day_meal}))
    assert response.status_code == 302
    updated_meal = Meal.objects.filter(plan_name=plan, plan_day=plan_day, meal=day_meal)
    assert updated_meal[0].meal_portions != meal.meal_portions



