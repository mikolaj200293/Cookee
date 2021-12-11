from django.contrib import admin

from .models import ProductCategory, Product, Recipe, Persons, Plan, Meal, ProductsQuantities, ShoppingList, \
    ShoppingListProducts


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


class ProductsQuantitiesAdmin(admin.ModelAdmin):
    pass


class ShoppingListAdmin(admin.ModelAdmin):
    pass


class ShoppingListProductsAdmin(admin.ModelAdmin):
    pass


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Persons, PersonsAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(ProductsQuantities, ProductsQuantitiesAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(ShoppingListProducts, ShoppingListProductsAdmin)

