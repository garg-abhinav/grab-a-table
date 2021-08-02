from django.urls import path, include
from . import views
from .views import Advanced, AllOrders, Dashboard, Inventory, OrderDetails, Recipe, AllOrders


urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('allorders/', AllOrders.as_view(), name='allorders'),
    path('advanced/', Advanced.as_view(), name='advanced'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('inventory-insert/', views.inventory_form,name='inventory_insert'),
    path('inventory-update/<int:id>/', views.inventory_form,name='inventory_update'),
    path('inventory-delete/<int:id>/',views.inventory_delete,name='inventory_delete'),
    path('inventory-list/',views.inventory_list,name='inventory_list'),
    path('recipe-insert/', views.recipe_form,name='recipe_insert'),
    path('recipe-update/<int:id>/', views.recipe_form,name='recipe_update'),
    path('recipe-delete/<int:id>/',views.recipe_delete,name='recipe_delete'),
    path('recipe-list/',views.recipe_list,name='recipe_list'),
]
