from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views import View
from main_app.models import Product, Recipe, Persons, Plan, Meal, ProductsQuantities, ShoppingList, \
    ShoppingListProducts
from main_app.forms import LoginForm, AddUserForm, ProductForm, RecipeForm, PlanForm, MealForm, \
    QuantitiesForm, PersonsForm
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


class HomeView(View):
    """
    Homepage view: shows base.html
    """

    def get(self, request):
        return TemplateResponse(request, 'main_app/base.html')


class LoginView(View):
    """
    Allows to login. In case of wrong login data reports the error.
    """

    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/login_form.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            logged_user = authenticate(username=username, password=password)
            if logged_user:
                login(request, logged_user)
                url_next = request.GET.get('next', '/home')
                return redirect(url_next)
            else:
                ctx['message'] = 'Błędne dane logowania'
                return TemplateResponse(request, 'main_app/login_form.html', ctx)
        else:
            return TemplateResponse(request, 'main_app/login_form.html', ctx)


class LogoutView(View):
    """
    Allow to logout
    """

    def get(self, request):
        logout(request)
        return TemplateResponse(request, 'main_app/base.html')


class AddUserView(View):
    """
    Allow to add new user.
    """

    def get(self, request):
        form = AddUserForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_user_form.html', ctx)

    def post(self, request):
        form = AddUserForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            confirmed_password = form.cleaned_data['confirm_password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['mail']
            if User.objects.filter(username=username).exists():
                ctx['error_message'] = 'Taki użytkownik już istnieje'
                return TemplateResponse(request, 'main_app/add_user_form.html', ctx)
            elif password != confirmed_password:
                ctx['error_message'] = 'Podane hasła różnią się'
                return TemplateResponse(request, 'main_app/add_user_form.html', ctx)
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                last_name=last_name, email=email)
                ctx['message'] = 'Dodano użytkownika'
                login(request, user)
                return redirect('home')
        else:
            return TemplateResponse(request, 'main_app/add_user_form.html', ctx)


class ProductsView(View):
    def get(self, request):
        products = Product.objects.all()
        ctx = {
            'products': products
        }
        return TemplateResponse(request, 'main_app/products.html', ctx)


class RecipesView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        ctx = {
            'recipes': recipes
        }
        return TemplateResponse(request, 'main_app/recipes.html', ctx)


class PlansView(View):
    def get(self, request):
        plans = Plan.objects.all()
        ctx = {
            'plans': plans
        }
        return TemplateResponse(request, 'main_app/plans.html', ctx)


class PersonsView(View):
    def get(self, request):
        persons = Persons.objects.all()
        ctx = {
            'persons': persons
        }
        return TemplateResponse(request, 'main_app/persons.html', ctx)


class PersonCreate(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/persons'

    def get(self, request):
        form = PersonsForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_person_form.html', ctx)

    def post(self, request):
        form = PersonsForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            name = form.cleaned_data['name']
            calories = form.cleaned_data['calories']
            user = request.user
            Persons.objects.create(name=name, calories=calories, user=user)
            persons = Persons.objects.all()
            ctx['persons'] = persons
            return TemplateResponse(request, 'main_app/persons.html', ctx)
        else:
            return TemplateResponse(request, 'main_app/persons.html', ctx)


class PersonDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Persons
    success_url = '/persons'


class PersonUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    success_url = '/persons'

    form_class = PersonsForm
    model = Persons
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return Persons.objects.get(pk=self.kwargs['person_id'])

    def get_success_url(self):
        return reverse("persons")


class RecipeCreate(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/add_recipe'

    def get(self, request):
        form = RecipeForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_recipe_form.html', ctx)

    def post(self, request):
        form = RecipeForm(request.POST)
        ctx = {
            'form': form
        }
        if form.is_valid():
            recipe_name = form.cleaned_data['recipe_name']
            description = form.cleaned_data['description']
            preparation_time = form.cleaned_data['preparation_time']
            products = form.cleaned_data['products']
            portions = form.cleaned_data['portions']
            instance = Recipe.objects.create(recipe_name=recipe_name, description=description,
                                             preparation_time=preparation_time, portions=portions)
            instance.products.set(products)
            ctx['recipe'] = instance
            recipe_id = instance.pk
            return redirect(reverse('recipe-details', kwargs={"recipe_id": recipe_id}), ctx)
        else:
            return TemplateResponse(request, 'main_app/add_recipe_form.html', ctx)


class RecipeDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Recipe
    success_url = '/recipes'


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    success_url = '/recipes'

    form_class = RecipeForm
    model = Recipe
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return Recipe.objects.get(pk=self.kwargs['recipe_id'])

    def get_success_url(self):
        return reverse("recipes")


class ProductCreate(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/add_product'

    def get(self, request):
        form = ProductForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_product_form.html', ctx)

    def post(self, request):
        form = ProductForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            proteins = form.cleaned_data['proteins']
            carbohydrates = form.cleaned_data['carbohydrates']
            fats = form.cleaned_data['fats']
            category = form.cleaned_data['category']
            Product.objects.create(product_name=product_name, proteins=proteins, carbohydrates=carbohydrates,
                                   fats=fats, category=category)
            products = Product.objects.all()
            ctx['products'] = products
            return TemplateResponse(request, 'main_app/products.html', ctx)
        else:
            return TemplateResponse(request, 'main_app/products.html', ctx)


class ProductDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Product
    success_url = '/products'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    success_url = '/products'

    form_class = ProductForm
    model = Product
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return Product.objects.get(pk=self.kwargs['product_id'])

    def get_success_url(self):
        return reverse("products")


class PlanCreate(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/add_plan'

    def get(self, request):
        form = PlanForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_plan_form.html', ctx)

    def post(self, request):
        form = PlanForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            plan_name = form.cleaned_data['plan_name']
            plan_length = form.cleaned_data['plan_length']
            persons = form.cleaned_data['persons']
            user = request.user
            instance = Plan.objects.create(plan_name=plan_name, plan_length=plan_length, user=user)
            instance.persons.set(persons)
            plans = Plan.objects.all()
            ctx['plans'] = plans
            return TemplateResponse(request, 'main_app/plans.html', ctx)
        else:
            return TemplateResponse(request, 'main_app/plans.html', ctx)


class PlanDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Plan
    success_url = '/plans'


class PlanUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    success_url = '/plans'

    form_class = PlanForm
    model = Plan
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        return Plan.objects.get(pk=self.kwargs['plan_id'])

    def get_success_url(self):
        return reverse("plans")


def calculate_days_calories(plan):
    days_calories_list = []
    for day in range(1, plan.plan_length + 1):
        day_meals = plan.meal_set.filter(plan_day=day)
        day_calories = 0
        for meal in day_meals:
            day_calories += meal.meal_portions * meal.recipes.portion_calories
        days_calories_list.append(round(day_calories, 2))
    return days_calories_list


class PlanDetailsView(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/add_plan'

    def get(self, request, plan_id):
        form = MealForm()
        plan = Plan.objects.get(pk=plan_id)
        meals = plan.meal_set.all()
        persons = plan.persons.all()
        plan_days = [day for day in range(1, plan.plan_length + 1)]
        days_calories_list = calculate_days_calories(plan)
        ctx = {
            'form': form,
            'plan': plan,
            'persons': persons,
            'meals': meals,
            'plan_days': plan_days,
            'days_calories': days_calories_list
        }
        return TemplateResponse(request, 'main_app/plan_details.html', ctx)

    def post(self, request, plan_id):
        form = MealForm(request.POST)
        plan = Plan.objects.get(pk=plan_id)
        persons = plan.persons.all()
        meals = plan.meal_set.all()
        plan_days = [day for day in range(1, plan.plan_length + 1)]
        days_calories_list = calculate_days_calories(plan)
        ctx = {
            'form': form,
            'plan': plan,
            'persons': persons,
            'meals': meals,
            'plan_days': plan_days,
            'days_calories': days_calories_list
        }
        if form.is_valid():
            plan_day = form.cleaned_data['plan_day']
            meal = form.cleaned_data['meal']
            recipes = form.cleaned_data['recipes']
            portions = form.cleaned_data['meal_portions']
            user = request.user
            meal_object = Meal.objects.filter(user=user, plan_name=plan, plan_day=plan_day, meal=meal)
            meal_calories = recipes.portion_calories * portions
            if meal_object.exists() and plan.plan_calories - calculate_days_calories(plan)[plan_day - 1] > meal_calories:
                meal_object.update(user=user, plan_day=plan_day, meal=meal, recipes=recipes, meal_portions=portions)
                days_calories_list = calculate_days_calories(plan)
                ctx['days_calories'] = days_calories_list
            elif meal_object.exists() and plan.plan_calories - calculate_days_calories(plan)[plan_day - 1] < meal_calories:
                ctx['message'] = 'Przekroczono limit kalorii'
            elif not meal_object and plan.plan_calories - calculate_days_calories(plan)[plan_day - 1] > meal_calories:
                instance = Meal.objects.create(user=user, plan_day=plan_day, meal=meal, recipes=recipes,
                                               meal_portions=portions)
                instance.plan_name.add(plan_id)
                days_calories_list = calculate_days_calories(plan)
                ctx['days_calories'] = days_calories_list
            elif not meal_object and plan.plan_calories - calculate_days_calories(plan)[plan_day - 1] < meal_calories:
                ctx['message'] = 'Przekroczono limit kalorii'
            return TemplateResponse(request, 'main_app/plan_details.html', ctx)
        else:
            return TemplateResponse(request, 'main_app/plan_details.html', ctx)


class MealDelete(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    success_url = '/plans'
    model = Meal

    def get_success_url(self):
        meal = Meal.objects.get(pk=self.kwargs['pk']).pk
        plan = Plan.objects.get(meal=meal)
        return f'/plan_details/{plan.pk}'

    def get_context_data(self, **kwargs):
        meal = Meal.objects.get(pk=self.kwargs['pk']).pk
        return {'plan': Plan.objects.get(meal=meal)}

    def get_object(self, queryset=None):
        return Meal.objects.get(pk=self.kwargs['pk'])


# class MealUpdate(LoginRequiredMixin, UpdateView):
#     login_url = '/login'
#     form_class = MealForm
#     model = Meal
#     template_name_suffix = '_update_form'
#
#     def get_success_url(self):
#         meal = Meal.objects.get(pk=self.kwargs['meal_id']).pk
#         plan = Plan.objects.get(meal=meal)
#         return f'/plan_details/{plan.pk}'
#
#     def get_object(self, queryset=None):
#         return Meal.objects.get(pk=self.kwargs['meal_id'])


class RecipeDetailsView(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/recipes'

    def get(self, request, recipe_id):
        form = QuantitiesForm()
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_products = recipe.products.all()
        recipe_products_quantities = recipe.productsquantities_set.all()
        form.fields['product_id'].queryset = recipe_products
        if recipe_products_quantities:
            form.initial = {'product_id': recipe_products_quantities[0]}
        ctx = {
            'form': form,
            'recipe': recipe,
            'products': recipe_products_quantities
        }
        return TemplateResponse(request, 'main_app/recipe_details.html', ctx)

    def post(self, request, recipe_id):
        form = QuantitiesForm(request.POST)
        recipe = Recipe.objects.get(pk=recipe_id)
        recipe_products = recipe.products.all()
        recipe_products_quantities = recipe.productsquantities_set.all()
        form.fields['product_id'].queryset = recipe_products
        if recipe_products:
            form.initial = {'product_id': recipe_products[0]}
        ctx = {
            'form': form,
            'recipe': recipe,
            'products': recipe_products_quantities
        }
        if form.is_valid():
            recipe = Recipe.objects.get(pk=recipe_id)
            product = form.cleaned_data['product_id']
            product_quantity = form.cleaned_data['product_quantity']
            ProductsQuantities.objects.filter(recipe_id=recipe, product_id=product). \
                update(product_quantity=product_quantity)
            return TemplateResponse(request, 'main_app/recipe_details.html', ctx)
        else:
            return TemplateResponse(request, 'main_app/recipe_details.html', ctx)


class ShoppingListCreate(LoginRequiredMixin, View):

    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        meals = plan.meal_set.all()
        ShoppingList.objects.create(name=f'Lista zakupów plan {plan.plan_name}', plan=plan)
        shopping_list = ShoppingList.objects.latest('date_created')
        for meal in meals:
            for product in meal.recipes.productsquantities_set.all():
                if not ShoppingListProducts.objects.filter(shopping_list=shopping_list.id,
                                                           product=product.product_id):
                    ShoppingListProducts.objects.create(shopping_list=shopping_list,
                                                        product_quantity=
                                                        product.one_portion_product_quantity * meal.meal_portions,
                                                        product=product.product_id)
                else:
                    ShoppingListProducts.objects.filter(shopping_list=shopping_list.id,
                                                        product=product.product_id).\
                        update(product_quantity=F('product_quantity') + product.
                               one_portion_product_quantity * meal.meal_portions)
        shopping_list_products = ShoppingListProducts.objects.filter(shopping_list=shopping_list)
        product_categories = []
        for product in shopping_list_products:
            if product.product.category.category_name not in product_categories:
                product_categories.append(product.product.category.category_name)
        ctx = {
            'shopping_list': shopping_list_products,
            'categories': product_categories
        }
        return TemplateResponse(request, 'main_app/shopping_list.html', ctx)


class ShoppingListPdf(LoginRequiredMixin, View):

    def get(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont('Arial', 14)
        textobject = p.beginText(2 * cm, 29.7 * cm - 2 * cm)
        shopping_list = ShoppingList.objects.latest('date_created')
        shopping_list_products = ShoppingListProducts.objects.filter(shopping_list=shopping_list)
        product_categories = []
        for product in shopping_list_products:
            if product.product.category.category_name not in product_categories:
                product_categories.append(product.product.category.category_name)
        pdf_string = ''
        for category in product_categories:
            pdf_string += f'{category}\n'
            for product in shopping_list_products:
                if product.product.category.category_name == category:
                    pdf_string += f'{product.product.product_name}, {product.product_quantity}g\n'
        for line in pdf_string.splitlines(False):
            textobject.textLine(line.rstrip())
        p.drawText(textobject)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='lista zakupów.pdf')


class PlanDayCaloriesCompletion(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/plans'

    def get(self, request, plan_id, plan_day, day_meal):
        plan_calories = Plan.objects.get(pk=plan_id).plan_calories
        plan_meals = Plan.objects.get(pk=plan_id).meal_set.filter(plan_day=plan_day)
        day_calories = 0
        for meal in plan_meals:
            day_calories += meal.meal_calories
        calories_to_fill = plan_calories - day_calories
        meal_to_fill = Meal.objects.get(plan_name=plan_id, plan_day=plan_day, meal=day_meal)
        meal_portion_calories = meal_to_fill.recipes.portion_calories
        portions_to_fill_quantity = round(calories_to_fill / meal_portion_calories, 1)
        meal_to_fill.meal_portions += portions_to_fill_quantity
        meal_to_fill.save()
        return redirect('plan-details', plan_id=plan_id)



