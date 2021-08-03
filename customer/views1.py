import json
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.db.models import Max
from django.core.mail import send_mail
from django.db import connection
from .models import Menu, Orders, Diners, Paymentmethod, Promotions, Cart


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class MenuView(View):
    def get(self, request, *args, **kwargs):
        menu_items = Menu.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = Menu.objects.filter(Q(food_item_desc__icontains=query))

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)

class OrderSearch(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'customer/order-search.html')

class Results(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("r")

        try:
            diner = Diners.objects.raw('SELECT * FROM deliver.Diners WHERE mobile_number = %s', [this])[0]
        except Diners.DoesNotExist:
             return render(request, 'customer/customer_orders.html')


        orders_list = Orders.objects.filter(mobile_number = diner)

        context = {
            'orders': orders_list
        }

        return render(request, 'customer/customer_orders.html', context)

class CustomerOrderDetails(View):
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

        return render(request, 'customer/customer_order_details.html', context)




class Order(View):
    def get(self, request, *args, **kwargs):
        
        temp = Menu.objects.all()

        # pass into context
        context = {
            'lists': temp,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        promo = request.POST.get('promo_code')
        payment_method = request.POST.get('payment_method')
        payment_description = request.POST.get('payment_description')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = Menu.objects.get(food_item_id=int(item))
            item_data = {
                'id': menu_item.food_item_id,
                'name': menu_item.food_item_desc,
                'price': menu_item.base_price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        diner, temp = Diners.objects.get_or_create(mobile_number=mobile_number)
        bill, temp = Paymentmethod.objects.get_or_create(payment_method=payment_method, payment_desc=payment_description)
        
        try:
            promoObject = Promotions.objects.get(promo_code = promo)
        except Promotions.DoesNotExist:
            promoObject, temp = Promotions.objects.get_or_create(promo_code = 'NONE', discount_percent = 1)

        price = price
        
        id_next = Orders.objects.count()+1


        with connection.cursor() as x:
            x.execute('CALL OrderUpdate(%s, %s, %s, %s, %s, %s)', [id_next, 'preparing', mobile_number, price, id_next, payment_method])

        order = Orders.objects.get(order_id = id_next)
        for id in item_ids:
            item = Menu.objects.filter(food_item_id = id)[0]
            Cart.objects.create(
                food_item = item, 
                order = order,
                qty = 1
            )

            with connection.cursor() as c:
                c.execute('CALL InventoryUpdate(%s, %s, %s)', [id_next, id, 1])
    
        

        
        
        context = {
            'items': order_items['items'],
            'price': order.total_billed_amount
        }

        return redirect('order-confirmation', pk=order.order_id)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order1 = Orders.objects.get(order_id=pk)
        set = Cart.objects.filter(order = order1)
        food = []
        for item in set:
            food.append(item.food_item)
        

        context = {
            'pk': order1.order_id,
            'items': food,
            'price': order1.total_billed_amount,
        }

        return render(request, 'customer/order_confirmation.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        if 'checkout' in request.POST:
            print("YES")
            return redirect('/menu/')