from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Login')
    password = forms.CharField(max_length=100, label='Hasło', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    login = forms.CharField(max_length=100, label='Login')
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label='First name')
    last_name = forms.CharField(max_length=100, label='Last name')
    mail = forms.EmailField(max_length=100, label='Email')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['add_date']
        localized_fields = '__all__'


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['add_date', 'edit_date']
        widgets = {
            'products': forms.CheckboxSelectMultiple,
        }
        localized_fields = '__all__'


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        exclude = ['user']
        widgets = {
            'persons': forms.CheckboxSelectMultiple,
        }
        localized_fields = '__all__'


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ['plan_name', 'user']

    plan_day = forms.IntegerField(min_value=1, label='Dzień planu')
    localized_fields = '__all__'


class QuantitiesForm(forms.ModelForm):
    class Meta:
        model = ProductsQuantities
        exclude = ['recipe_id']

    field_order = ['product_id', 'product_quantity']
    localized_fields = '__all__'


class PersonsForm(forms.ModelForm):
    class Meta:
        model = Persons
        exclude = ['user']
        localized_fields = '__all__'
