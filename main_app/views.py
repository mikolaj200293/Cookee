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
from main_app.functions import calculate_days_calories

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))


class HomeView(View):
    """
    Homepage view: show base.html
    """

    def get(self, request):
        return TemplateResponse(request, 'main_app/base.html')


class LoginView(View):
    """
    Login user. In case of wrong login data report the error.
    """

    def get(self, request):
        """
        Redirect to login form.
        :param request: django request object
        :return: redirect to login_form.html with LoginForm in context
        """
        form = LoginForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/login_form.html', ctx)

    def post(self, request):
        """
        Validate login form. If form is valid authenticate user. If authentication was successful log user in
        and redirect to home page. If authentication failed show error message and redirect to login page.
        If login form is not valid stay on login page.
        :param request: django request object
        :return: redirect to base.html or to login_form.html with LoginForm and additional data in context
        """
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
    Logout the user.
    """

    def get(self, request):
        """
        Logout the user and redirect to home page.
        :param request: django request object
        :return: redirect to base.html
        """
        logout(request)
        return TemplateResponse(request, 'main_app/base.html')


class AddUserView(View):
    """
    Add new user.
    """

    def get(self, request):
        """
        Redirect to user adding form.
        :param request: django request object
        :return: redirect to add_user_form.html with AddUserForm in context
        """
        form = AddUserForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_user_form.html', ctx)

    def post(self, request):
        """
        Validate user adding form. If form is valid check if user exist and sent passwords are the same.
        If correct create new User object and log new User in. If form is not valid stay on add_user_form.html
        :param request: django request object
        :return: if User object created redirect to home.html else redirect to add_user_form.html with AddUserForm
        and additional data in context
        """
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
    """
    Show all Product model objects.
    """

    def get(self, request):
        """
        Get all Product model object and send them to products.html in context
        :param request: django request object
        :return: redirects to products.html with context data
        """
        products = Product.objects.all()
        ctx = {
            'products': products
        }
        return TemplateResponse(request, 'main_app/products.html', ctx)


class RecipesView(View):
    """
    Show all Recipe model objects.
    """

    def get(self, request):
        """
        Get all Recipe model object and send them to recipes.html in context
        :param request: django request object
        :return: redirect to recipes.html with context data
        """
        recipes = Recipe.objects.all()
        ctx = {
            'recipes': recipes
        }
        return TemplateResponse(request, 'main_app/recipes.html', ctx)


class PlansView(View):
    """
    Show all Plan model objects
    """

    def get(self, request):
        """
        Get all Plan model object and send them to plans.html in context
        :param request: django request object
        :return: redirect to plans.html with context data
        """
        plans = Plan.objects.all()
        ctx = {
            'plans': plans
        }
        return TemplateResponse(request, 'main_app/plans.html', ctx)


class PersonsView(View):
    """
    Show all Persons model objects
    """

    def get(self, request):
        """
        Get all Persons model object and send them to persons.html in context
        :param request: django request object
        :return: redirect to persons.html with context data
        """
        persons = Persons.objects.all()
        ctx = {
            'persons': persons
        }
        return TemplateResponse(request, 'main_app/persons.html', ctx)


class PersonCreate(LoginRequiredMixin, View):
    """
    Create new Persons object. Require logged-in user.
    """
    login_url = '/login'
    success_url = '/persons'

    def get(self, request):
        """
        Redirect to Persons model object adding form.
        :param request: django request object
        :return: redirect to add_person_form.html with PersonsForm in context
        """
        form = PersonsForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_person_form.html', ctx)

    def post(self, request):
        """
        Validate PersonsForm. If form is valid create new Persons model object and redirect to persons.html.
        If form is not valid redirect to add_person_form.html
        :param request: django request object
        :return: If Persons object created redirect to persons.html. If Persons object not created redirect
        to add_person_form.html
        """
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
            return TemplateResponse(request, 'main_app/add_person_form.html', ctx)


class PersonDelete(LoginRequiredMixin, DeleteView):
    """
    Delete Persons model object. Require logged-in user. Redirect to /persons.
    """
    login_url = '/login'
    model = Persons
    success_url = '/persons'


class PersonUpdate(LoginRequiredMixin, UpdateView):
    """
    Update Persons model object. Require logged-in user. Redirect to /persons.
    """
    login_url = '/login'
    success_url = '/persons'

    form_class = PersonsForm
    model = Persons
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        """
        Select Persons object to update
        :param queryset: built-in parameter
        :return: Persons model object to update
        """
        return Persons.objects.get(pk=self.kwargs['person_id'])

    def get_success_url(self):
        """
        Define Url to redirect after Persons model object update
        :return: Url to redirect after update
        """
        return reverse("persons")


class RecipeCreate(LoginRequiredMixin, View):
    """
    Create new Recipe model object. Require logged-in user.
    """
    login_url = '/login'
    success_url = '/add_recipe'

    def get(self, request):
        """
        Redirect to Recipe model object adding form.
        :param request: django request object
        :return: redirect to add_recipe_form.html with RecipeForm in context
        """
        form = RecipeForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_recipe_form.html', ctx)

    def post(self, request):
        """
        Validate RecipeForm data. If form is valid create new Recipe model object and redirect to recipe_details.html
        with new recipe object in context. If form is not valid redirect to add_recipe_form.html
        :param request: django request object
        :return: If Recipe object model created redirect to recipe_details.html. If Recipe model object not created
        redirect to add_recipe_form.html
        """
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
    """
    Delete Recipe model object. Require logged-in user. Redirect to /recipes.
    """
    login_url = '/login'
    model = Recipe
    success_url = '/recipes'


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    """
    Update Recipe model object. Require logged-in user. Redirect to /recipes.
    """
    login_url = '/login'
    success_url = '/recipes'

    form_class = RecipeForm
    model = Recipe
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        """
        Select Recipe object to update
        :param queryset: built-in parameter
        :return: Recipe model object to update
        """
        return Recipe.objects.get(pk=self.kwargs['recipe_id'])

    def get_success_url(self):
        """
        Define Url to redirect after Recipe model object update
        :return: Url to redirect after update
        """
        return reverse("recipes")


class ProductCreate(LoginRequiredMixin, View):
    """
    Create new Product model object. Require logged-in user.
    """
    login_url = '/login'
    success_url = '/add_product'

    def get(self, request):
        """
        Redirect to Product model object adding form.
        :param request: django request object
        :return: redirect to add_product_form.html with ProductForm in context
        """
        form = ProductForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_product_form.html', ctx)

    def post(self, request):
        """
        Validate ProductForm data. If form is valid create new Product model object and redirect to products.html
        with all Recipe model objects in context. If form is not valid redirect to add_product_form.html
        :param request: django request object
        :return: If Product model object created redirect to products.html. If Product model object not created redirect
        to add_recipe_form.html
        """
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
            return TemplateResponse(request, 'main_app/add_product_form.html', ctx)


class ProductDelete(LoginRequiredMixin, DeleteView):
    """
    Delete Product model object. Require logged-in user. Redirect to /products.
    """
    login_url = '/login'
    model = Product
    success_url = '/products'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    """
    Update Product model object. Require logged-in user. Redirect to /products.
    """
    login_url = '/login'
    success_url = '/products'

    form_class = ProductForm
    model = Product
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        """
        Select Product object to update
        :param queryset: built-in parameter
        :return: Product model object to update
        """
        return Product.objects.get(pk=self.kwargs['product_id'])

    def get_success_url(self):
        """
        Define Url to redirect after Product model object update
        :return: Url to redirect after update
        """
        return reverse("products")


class PlanCreate(LoginRequiredMixin, View):
    """
    Create Plan mode object. Require logged-in user.
    """
    login_url = '/login'
    success_url = '/add_plan'

    def get(self, request):
        """
        Redirect to Plan model object adding form.
        :param request: django request object
        :return: redirect to add_plan_form.html with PlanForm in context
        """
        form = PlanForm()
        ctx = {
            'form': form
        }
        return TemplateResponse(request, 'main_app/add_plan_form.html', ctx)

    def post(self, request):
        """
        Validate PlanForm data. If form is valid create new Plan model object and redirect to plans.html
        with all Plan model objects in context. If form is not valid redirect to add_plan_form.html
        :param request: django request object
        :return: If Plan model object created redirect to plans.html. If Plan model object not created redirect
        to add_plan_form.html
        """
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
            return TemplateResponse(request, 'main_app/add_plan_form.html', ctx)


class PlanDelete(LoginRequiredMixin, DeleteView):
    """
    Delete Plan model object. Require logged-in user. Redirect to /plans.
    """
    login_url = '/login'
    model = Plan
    success_url = '/plans'


class PlanUpdate(LoginRequiredMixin, UpdateView):
    """
    Update Plan model object. Require logged-in user. Redirect to /plans.
    """
    login_url = '/login'
    success_url = '/plans'

    form_class = PlanForm
    model = Plan
    template_name_suffix = '_update_form'

    def get_object(self, queryset=None):
        """
        Select Plan object to update
        :param queryset: built-in parameter
        :return: Plan model object to update
        """
        return Plan.objects.get(pk=self.kwargs['plan_id'])

    def get_success_url(self):
        """
        Define Url to redirect after Product model object update
        :return: Url to redirect after update
        """
        return reverse("plans")


class PlanDetailsView(LoginRequiredMixin, View):
    """
    Add and update Meal model object related to chosen Plan model object. Require logged-in user.
    """
    login_url = '/login'
    success_url = '/add_plan'

    def get(self, request, plan_id):
        """
        Create context data for plan_details.html. Redirect to plan_details.html.
        :param request: Django request object.
        :param plan_id: Plan model object primary key to which updated and created Meal objects are related.
        :return: Redirect to plan_details.html with MealForm and plan and meal objects data in context.
        """
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
        """
        Create context data for plan_details.html. Validate MealForm. If MealForm is valid create or update requested
        Meal model object. If MealForm is not valid redirect to plan_details.html.
        If Meal model object update check for calories amount. If new Meal model object calories amount exceed
        the calories left for use for plan_day add error message to context. If opposite update requested Meal model
        object.
        If Meal model object create check for calories amount. If new Meal model object calories amount exceed
        the calories left for use for plan_day add error message to context. If opposite create requested Meal model
        object.
        :param request: Django request object
        :param plan_id: Plan model object primary key to which updated and created Meal objects are related.
        :return: Redirect to plan_details.html with MealForm and plan and meal objects data and optionally error message
        in context.
        """
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
            if meal_object and ((plan.plan_calories - calculate_days_calories(plan)[plan_day - 1] > meal_calories) or
                                (plan.plan_calories - calculate_days_calories(plan)[plan_day - 1] < meal_calories <
                                 meal_object[0].meal_calories)):
                meal_object.update(user=user, plan_day=plan_day, meal=meal, recipes=recipes, meal_portions=portions)
                days_calories_list = calculate_days_calories(plan)
                ctx['days_calories'] = days_calories_list
            elif meal_object and plan.plan_calories - calculate_days_calories(plan)[
                plan_day - 1] < meal_calories and meal_calories > meal_object[0].meal_calories:
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
    """
    Delete Meal model object. Require logged-in user. Redirect to /plan_details/<plan_id>.
    """
    login_url = '/login'
    success_url = '/plans'
    model = Meal

    def get_success_url(self):
        """
        Define Url to redirect after Meal model object deletion
        :return: Url to redirect after update
        """
        meal = Meal.objects.get(pk=self.kwargs['pk']).pk
        plan = Plan.objects.get(meal=meal)
        return f'/plan_details/{plan.pk}'

    def get_context_data(self, **kwargs):
        """
        Create context data.
        :param kwargs: Built-in parameter
        :return: Context data with Plan model object
        """
        meal = Meal.objects.get(pk=self.kwargs['pk']).pk
        return {'plan': Plan.objects.get(meal=meal)}

    def get_object(self, queryset=None):
        """
        Select Meal object to delete
        :param queryset: Built-in parameter
        :return: Meal model object to delete
        """
        return Meal.objects.get(pk=self.kwargs['pk'])


class RecipeDetailsView(LoginRequiredMixin, View):
    """
    Set products quantities in ProductQuantities model object related to chosen Recipe model object.
    Require logged-in user.
    """
    login_url = '/login'
    success_url = '/recipes'

    def get(self, request, recipe_id):
        """
        Create context data for recipe_details.html. Redirect to recipe_details.html.
        :param request: Django request object.
        :param recipe_id: Recipe model object primary key to which updated ProductQuantities objects are related.
        :return: Redirect to recipe_details.html with QuantitiesForm and recipe and related products quantities
        data in context.
        """
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
        """
        Create context data for recipe_details.html. Validate QuantitiesForm. If MealForm is valid update requested
        ProductQuantities model object. If QuantitiesForm is not valid redirect to recipe_details.html.
        :param request: Django request object.
        :param recipe_id: Recipe model object primary key to which updated ProductQuantities objects are related.
        :return: Redirect to recipe_details.html with QuantitiesForm and recipe and related products quantities
        data in context.
        """
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
    """
    Create ShoppingList model object related to chosen Plan model object. Create and update ShoppingListProducts model
    objects related to created ShoppingList model object. Require logged-in user.
    """
    login_url = '/login'
    success_url = '/plans'

    def get(self, request, plan_id):
        """
        Create ShoppingList model object for related Plan model object. Set (create/update) ShoppingListProducts model
        object for created ShoppingList model object. Create context data for shopping_list.html. Redirect to
        shopping_list.html.
        :param request: Django request object.
        :param plan_id: Plan model object primary key to which created ShoppingList model objects are related.
        :return: Redirect to shopping_list.html with QuantitiesForm with shopping list products and products categories
        in context data.
        """
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
                                                        product=product.product_id). \
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
    """
    Generate .pdf file with ShoppingListProducts related to last created ShoppingList model object and download it.
    """
    login_url = '/login'
    success_url = '/plans'

    def get(self, request):
        """
        Create string with ShoppingListProducts model object data related to last created ShoppingList model object.
        Create .pdf file and save created string to it.
        :param request: Django request object
        :return: Download 'Lista zakupów.pdf'.
        """
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
        return FileResponse(buffer, as_attachment=True, filename='Lista zakupów.pdf')


class PlanDayCaloriesCompletion(LoginRequiredMixin, View):
    """
    Update Meal object portions parameter to fulfill plan day calories.
    """
    login_url = '/login'
    success_url = '/plans'

    def get(self, request, plan_id, plan_day, day_meal):
        """
        Check for calories gap in selected plan_day in relation to plan's persons calories sum. Update selected Meal
        model object portions parameter, to cover the calories gap.
        :param request: Django request object
        :param plan_id: Plan model object primary key to which updated Meal model objects are related.
        :param plan_day: Updated Meal model object plan_day parameter.
        :param day_meal: Updated Meal model meal parameter
        :return: Redirect to plan_details/<plan_id>.
        """
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
