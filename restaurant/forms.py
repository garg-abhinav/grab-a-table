from django import forms
from .models import Inventory, Recipe


class InventoryForm(forms.ModelForm):

    class Meta:
        model = Inventory
        fields = ('ingredient', 'qty_available', 'last_update_timestamp')
        labels = {
            'ingredient':'Ingredient',
            'qty_available':'Quantity',
            'last_update_timestamp':'Last Updated'
            
        }

    def __init__(self, *args, **kwargs):
        super(InventoryForm,self).__init__(*args, **kwargs)

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('food_item', 'ingredient', 'ingredient_quantity')
        labels = {
            'food_item':'Menu Item',
            'ingredient':'Ingredient',
            'ingredient_quantity':'Quantity',
            
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm,self).__init__(*args, **kwargs)