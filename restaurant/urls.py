"""arrowheads URL Configuration

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import Dashboard, AllOrders, OrderDetails, HistoricOrderDetails

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('allorders/', AllOrders.as_view(), name='allorders'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('historic-orders/<int:pk>/', HistoricOrderDetails.as_view(), name='historic-order-details'),
    path('inventory-insert/', views.inventory_form,name='inventory_insert'),
    path('inventory-update/<int:id>/', views.inventory_form,name='inventory_update'),
    path('inventory-delete/<int:id>/',views.inventory_delete,name='inventory_delete'),
    path('inventory-list/',views.inventory_list,name='inventory_list'),
    path('recipe-insert/', views.recipe_sheet,name='recipe_insert'),
    path('recipe-update/<int:id>/', views.recipe_sheet,name='recipe_update'),
    path('recipe-delete/<int:id>/',views.recipe_delete,name='recipe_delete'),
    path('recipe-list/',views.recipe_list,name='recipe_list'),

]
