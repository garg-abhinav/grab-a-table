from django.contrib import admin
from .models import Menu, Orders, Cart, Inventory, Ingredients, Diners, Paymentmethod, Promotions, Recipe

admin.site.register(Menu)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Inventory)
admin.site.register(Ingredients)
admin.site.register(Diners)
admin.site.register(Paymentmethod)
admin.site.register(Promotions)
admin.site.register(Recipe)
