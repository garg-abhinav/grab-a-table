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

def recipe_delete(request,id):
    recipe = Recipe.objects.get(pk=id)
    recipe.delete()
    
    return redirect('/restaurant/recipe-list')

def recipe_sheet(request, id=0):
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

    l = Inventory.objects.all().order_by('-inventory_id')[0:25]
    ingredients = []
    empty = []
    l = list(l)
    for item in l:
        if item.ingredient not in ingredients:
            item.qty_available = round(item.qty_available, 2)
            ingredients.append(item.ingredient)
            empty.append(item)

    context = {'inventory_list': empty}
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
    context = {'recipe_list': Recipe.objects.raw('SELECT * FROM deliver.Recipe LIMIT 50')}
    return render(request, "restaurant/recipe_list.html", context)


def recipe_forms(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = RecipeForm()
        else:
            recipe = Recipe.objects.get(pk=id)
            form = RecipeForm(instance=recipe)

        return render(request, "restaurant/recipe_form.html", {'form': form})
    else:
        food = request.POST.get('food_item')
        ingred = request.POST.get('ingredient')
        qty = request.POST.get('ingredient_qty')

        if id == 0:
            Recipe.objects.raw('INSERT INTO deliver.Recipe VALUES %s, %s, %s', [food, ingred, qty])
        else:
            Recipe.objects.raw('UPDATE deliver.Recipe SET food_item = %s, ingredient = %s, ingredient_quantity = %s WHERE pk = %s', [food, ingred, qty, id])

        return redirect('/restaurant/recipe-list')


def recipe_deletes(request,id):
    #recipe = Recipe.objects.get(pk=id)
    #recipe.delete()
    Recipe.objects.raw('DELETE FROM deliver.Recipe WHERE pk = %s', [id])

    
    return redirect('/restaurant/recipe-list')

class Advanced(View):
    def get(self, request, *args, **kwargs):

        #orders1 = .objects.raw('SELECT * FROM badDays')
        #orders2 = Orders.objects.values('order_completed_at').annotate(avg_rating = Avg('rating'), count = Count("order_id")).order_by('-count')
        #print(orders1)

        dict = {}
        temp = {}
        x = []

        bad = Orders.objects.raw('SELECT * FROM Orders WHERE rating <=3')
        for l in bad:
            r = Cart.objects.filter(order = l.order_id)
            for item in r:
                x.append(item.food_item.food_item_desc)
        print(x)

        for food in x:
            dict[food] = dict.get(food, 0)+1
        print(dict)

        temp = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        print(temp)

        # pass total number of orders and total revenue into template
        context = {
            'poor': temp
        }

        return render(request, 'restaurant/output1.html', context)