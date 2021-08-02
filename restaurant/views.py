from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from django.db.models import Q
from django.db.models import Count, Avg
from datetime import date
import calendar
from customer.models import Menu, Orders, Diners, Paymentmethod, Promotions, Cart, Inventory, Recipe
from .forms import InventoryForm, RecipeForm


class Dashboard(View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        print(today.weekday())
        orders = Orders.objects.filter(
            order_placed_at__year=today.year, order_placed_at__month=today.month, order_placed_at__day=today.day)

        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.total_billed_amount
            if order.order_status == 'preparing':
                unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': round(total_revenue, 2),
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard.html', context)

class AllOrders(View):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        print(today.weekday())
        orders = Orders.objects.all()

        # loop through the orders and add the price value, check if order is not shipped
        unshipped_orders = []
        total_revenue = 0
        for order in orders:
            total_revenue += order.total_billed_amount
            unshipped_orders.append(order)

        # pass total number of orders and total revenue into template
        context = {
            'orders': unshipped_orders,
            'total_revenue': round(total_revenue, 2),
            'total_orders': len(orders)
        }

        return render(request, 'restaurant/dashboard1.html', context)

class OrderDetails(View):
    def get(self, request, pk, *args, **kwargs):
        order1 = Orders.objects.get(order_id=pk)
        set = Cart.objects.filter(order = order1)
        food = []
        for item in set:
            food.append(item.food_item)
        
        
        context = {
            'food': food,
            'order': order1
        }

        return render(request, 'restaurant/order-details.html', context)

    def post(self, request, pk, *args, **kwargs):
        order = Orders.objects.get(pk=pk)
        order.order_status='completed'
        order.order_completed_at = datetime.now()
        order.save()

        context = {
            'order': order
        }

        return render(request, 'restaurant/order-details.html', context)

class HistoricOrderDetails(View):
    def get(self, request, pk, *args, **kwargs):
        order1 = Orders.objects.get(order_id=pk)
        set = Cart.objects.filter(order = order1)
        food = []
        for item in set:
            food.append(item.food_item)
        
        
        context = {
            'food': food,
            'order': order1
        }

        return render(request, 'restaurant/order-details1.html', context)

def inventory_list(request):
    context = {'inventory_list': Inventory.objects.all()}
    return render(request, "restaurant/inventory_list.html", context)


def inventory_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = InventoryForm()
        else:
            inventory = Inventory.objects.get(pk=id)
            form = InventoryForm(instance=inventory)
        return render(request, "restaurant/inventory_form.html", {'form': form})
    else:
        if id == 0:
            form = InventoryForm(request.POST)
        else:
            inventory = Inventory.objects.get(pk=id)
            form = InventoryForm(request.POST,instance= inventory)
        if form.is_valid():
            form.save()
        return redirect('/restaurant/inventory-list')

def inventory_delete(request,id):
    inventory = Inventory.objects.get(pk=id)
    inventory.delete()
    return redirect('/restaurant/inventory-list')

def recipe_list(request):
    context = {'recipe_list': Recipe.objects.all()}
    return render(request, "restaurant/recipe_list.html", context)


def recipe_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = RecipeForm()
        else:
            recipe = Recipe.objects.get(pk=id)
            form = RecipeForm(instance=recipe)
        return render(request, "restaurant/recipe_form.html", {'form': form})
    else:
        if id == 0:
            form = RecipeForm(request.POST)
        else:
            recipe = Recipe.objects.get(pk=id)
            form = RecipeForm(request.POST,instance= recipe)
        if form.is_valid():
            form.save()
        return redirect('/restaurant/recipe-list')


def recipe_delete(request,id):
    recipe = Recipe.objects.get(pk=id)
    recipe.delete()
    return redirect('/restaurant/recipe-list')