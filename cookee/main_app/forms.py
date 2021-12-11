from django import forms
from .models import ProductCategory, Product, Recipe, Plan, Meal, ProductsQuantities, Persons


class LoginForm(forms.Form):
    """
    Create user login form.
    """
    username = forms.CharField(max_length=100, label='Login')
    password = forms.CharField(max_length=100, label='Hasło', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    """
    Create user creating form.
    """
    login = forms.CharField(max_length=100, label='Nazwa użytkownika')
    password = forms.CharField(max_length=100, label='Hasło', widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, label='Potwierdź hasło', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label='Imię')
    last_name = forms.CharField(max_length=100, label='Nazwisko')
    mail = forms.EmailField(max_length=100, label='Adres Email')


class CategoryForm(forms.ModelForm):
    """
    Create form for ProductCategory model.
    """
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductForm(forms.ModelForm):
    """
    Create form for Product model.
    """
    class Meta:
        model = Product
        exclude = ['add_date']
        localized_fields = '__all__'


class RecipeForm(forms.ModelForm):
    """
    Create form for Recipe model.
    """
    class Meta:
        model = Recipe
        exclude = ['add_date', 'edit_date']
        widgets = {
            'products': forms.CheckboxSelectMultiple,
        }
        localized_fields = '__all__'


class PlanForm(forms.ModelForm):
    """
    Create form for Plan model.
    """
    class Meta:
        model = Plan
        exclude = ['user']
        widgets = {
            'persons': forms.CheckboxSelectMultiple,
        }
        localized_fields = '__all__'


class MealForm(forms.ModelForm):
    """
    Create form for Meal model.
    """
    class Meta:
        model = Meal
        exclude = ['plan_name', 'user']

    plan_day = forms.IntegerField(min_value=1, label='Dzień planu')
    localized_fields = '__all__'


class QuantitiesForm(forms.ModelForm):
    """
    Create form for ProductQuantities model.
    """
    class Meta:
        model = ProductsQuantities
        exclude = ['recipe_id']

    field_order = ['product_id', 'product_quantity']
    localized_fields = '__all__'


class PersonsForm(forms.ModelForm):
    """
    Create form for Persons model.
    """
    class Meta:
        model = Persons
        exclude = ['user']
        localized_fields = '__all__'
