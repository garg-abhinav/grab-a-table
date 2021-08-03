# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models 


class Cart(models.Model):
    food_item = models.ForeignKey('Menu', on_delete=models.CASCADE)
    order = models.ForeignKey('Orders',   on_delete=models.CASCADE)
    qty = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Cart'
        unique_together = (('food_item', 'order'),)


class Diners(models.Model):
    mobile_number = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Diners'


class Ingredients(models.Model):
    ingredient_id = models.IntegerField(primary_key=True)
    ingredient_desc = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Ingredients'

    def __str__(self):
        return self.ingredient_desc


class Inventory(models.Model):
    inventory_id = models.IntegerField(primary_key=True)
    last_update_timestamp = models.DateTimeField(blank=True, null=True)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    qty_available = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'Inventory'
        unique_together = (('last_update_timestamp', 'ingredient'),)


class Menu(models.Model):
    food_item_id = models.IntegerField(primary_key=True)
    food_item_desc = models.TextField(blank=True, null=True)
    cuisine = models.CharField(max_length=20, blank=True, null=True)
    food_type = models.CharField(max_length=20, blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    base_price = models.FloatField(blank=True, null=True)
    availability = models.IntegerField(blank=True, null=True)
    prep_instructions = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Menu'
    
    def __str__(self):
        return self.food_item_desc


class Orders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_placed_at = models.DateTimeField(auto_now_add=True, null=True)
    order_completed_at = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(max_length=50, blank=True, null=True,  default='preparing')
    mobile_number = models.ForeignKey(Diners,   db_column='mobile_number', blank=True, null=True, on_delete=models.CASCADE)
    total_billed_amount = models.FloatField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=30, blank=True, null=True)
    payment_method = models.ForeignKey('Paymentmethod',   db_column='payment_method', blank=True, null=True, on_delete=models.CASCADE)
    promo_code = models.ForeignKey('Promotions', db_column='promo_code', blank=True, null=True, on_delete=models.CASCADE)
    net_payable = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'Orders'


class Paymentmethod(models.Model):
    payment_method = models.CharField(primary_key=True, max_length=50)
    payment_desc = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'PaymentMethod'
    
    def __str__(self):
        return self.payment_desc


class Promotions(models.Model):
    promo_code = models.CharField(primary_key=True, max_length=10)
    promo_desc = models.TextField(blank=True, null=True)
    discount_percent = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Promotions'


class Recipe(models.Model):
    food_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients,   on_delete=models.CASCADE)
    ingredient_quantity = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'Recipe'
        unique_together = (('food_item', 'ingredient'),)
