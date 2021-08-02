from django.contrib import admin
from .models import Menu, Orders, Cart, Inventory, Ingredients, Diners, Paymentmethod

admin.site.register(Menu)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Inventory)
admin.site.register(Ingredients)
admin.site.register(Diners)
admin.site.register(Paymentmethod)
