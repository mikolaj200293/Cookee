from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import FormView
from .models import *
from .forms import *
from django.views.generic import *
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import *


class HomeView(View):
    def get(self, request):
        return TemplateResponse(request, 'main_app/base.html')


class LoginView(View):
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
        return render(request, "main_app/login_form.html", ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return TemplateResponse(request, 'main_app/base.html')


class AddUserView(View):
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


class RecipeCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    success_url = '/add_recipe'

    form_class = RecipeForm
    template_name = "main_app/add_recipe_form.html"

    # def get(self, request):
    #     form = RecipeForm()
    #     ctx = {
    #         'form': form
    #     }
    #     return TemplateResponse(request, 'main_app/add_recipe_form.html', ctx)
    #
    # def post(self, request):
    #     form = RecipeForm(request.POST)
    #     ctx = {
    #         'form': form
    #     }
    #     if form.is_valid():
    #         recipe_name = form.cleaned_data['recipe_name']
    #         description = form.cleaned_data['description']
    #         preparation_time = form.cleaned_data['preparation_time']
    #         products = form.cleaned_data['products']
    #         portions = form.cleaned_data['portions']
    #         quantities = 0
    #         instance = Recipe.objects.create(recipe_name=recipe_name, description=description,
    #                                          preparation_time=preparation_time, portions=portions)
    #         instance.products.set(products)
    #         ctx['recipe'] = instance
    #         return TemplateResponse(request, 'main_app/add_recipe_form.html', ctx)


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
            if float(proteins) + float(carbohydrates) + float(fats) == 100:
                Product.objects.create(product_name=product_name, proteins=proteins, carbohydrates=carbohydrates,
                                       fats=fats, category=category)
                products = Product.objects.all()
                ctx['products'] = products
                return TemplateResponse(request, 'main_app/products.html', ctx)
            else:
                ctx['error_message'] = 'Suma składników makro musi wynosić 100'
                return TemplateResponse(request, 'main_app/add_product_form.html', ctx)


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


class PlanDetailsView(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/add_plan'

    def get(self, request, plan_id):
        form = MealForm()
        plan = Plan.objects.get(pk=plan_id)
        meals = plan.meal_set.all()
        persons = plan.persons.all()
        calories = 0
        for person in persons:
            calories += float(person.calories)
        ctx = {
            'form': form,
            'plan': plan,
            'persons': persons,
            'meals': meals,
            'calories': calories
        }
        return TemplateResponse(request, 'main_app/plan_details.html', ctx)

    def post(self, request, plan_id):
        form = MealForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            plan = Plan.objects.get(pk=plan_id)
            persons = plan.persons.all()
            plan_day = form.cleaned_data['plan_day']
            meal = form.cleaned_data['meal']
            recipes = form.cleaned_data['recipes']
            user = request.user
            instance = Meal.objects.create(user=user, plan_day=plan_day, meal=meal, recipes=recipes)
            instance.plan_name.add(plan_id)
            ctx['plan'] = plan
            ctx['persons'] = persons
            return TemplateResponse(request, 'main_app/plan_details.html', ctx)


class RecipeDetailsView(LoginRequiredMixin, View):
    login_url = '/login'
    success_url = '/add_plan'

    def get(self, request, recipe_id):
        form = QuantitiesForm()
        recipe = Recipe.objects.get(pk=recipe_id)
        ctx = {
            'form': form,
            'recipe': recipe
        }
        return TemplateResponse(request, 'main_app/recipe_details.html', ctx)