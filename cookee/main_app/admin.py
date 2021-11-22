from django.contrib import admin

from .models import *


class ProductCategoryAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    pass


class PersonsAdmin(admin.ModelAdmin):
    pass


class PlanAdmin(admin.ModelAdmin):
    pass


class MealAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Persons, PersonsAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Meal, MealAdmin)
