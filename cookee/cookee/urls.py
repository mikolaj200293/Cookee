"""cookee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', HomeView.as_view(), name='home'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('add_user', AddUserView.as_view(), name='add-user'),
    path('products', ProductsView.as_view(), name='products'),
    path('recipes', RecipesView.as_view(), name='recipes'),
    path('plans', PlansView.as_view(), name='plans'),
    path('add_recipe', RecipeCreate.as_view(), name='add-recipe'),
    path('add_product', ProductCreate.as_view(), name='add-product'),
    path('add_plan', PlanCreate.as_view(), name='add-plan'),
    path('delete_product/<pk>', ProductDelete.as_view(), name='delete-product'),
    path('delete_recipe/<pk>', RecipeDelete.as_view(), name='delete-recipe'),
    path('edit_product/<int:product_id>', ProductUpdate.as_view(), name='edit-product'),
    path('edit_recipe/<int:recipe_id>', RecipeUpdate.as_view(), name='edit-recipe'),
    path('plan_details/<int:plan_id>', PlanDetailsView.as_view(), name='plan-details'),
    path('recipe_details/<int:recipe_id>', RecipeDetailsView.as_view(), name='recipe-details'),
]
