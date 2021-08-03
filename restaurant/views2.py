from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.utils.timezone import datetime
from django.db.models import Q
from django.db.models import Count, Avg
from datetime import date
import calendar
from customer.models import Menu, Orders, Diners, Paymentmethod, Promotions, Cart, Inventory, Recipe

import pickle
import pandas as pd
import numpy as np
import datetime

def get_features(df, date_col):
    months_in_year = 12
    days_in_week = 7
    weeks_in_year = 52
    feats = ['order_date_sin_moy', 'order_date_cos_moy', 'order_date_sin_dow', 
             'order_date_cos_dow', 'order_date_sin_woy', 'order_date_cos_woy']
    df['order_date'] = pd.to_datetime(df[date_col])
    df['order_date' + '_sin_moy'] = np.sin(2*np.pi*df['order_date'].dt.month/months_in_year)
    df['order_date' + '_cos_moy'] = np.cos(2*np.pi*df['order_date'].dt.month/months_in_year)
    df['order_date' + '_sin_dow'] = np.sin(2*np.pi*df['order_date'].dt.weekday/days_in_week)
    df['order_date' + '_cos_dow'] = np.cos(2*np.pi*df['order_date'].dt.weekday/days_in_week)
    df['order_date' + '_sin_woy'] = np.sin(2*np.pi*df['order_date'].dt.isocalendar().week/weeks_in_year)
    df['order_date' + '_cos_woy'] = np.cos(2*np.pi*df['order_date'].dt.isocalendar().week/weeks_in_year)
    return df[feats].values

def predict(ingredient_id, date):
    # date should be a datetime datatype
    # returns qty needed for next 7 days starting the date passed as a list
    dates = []
    for i in range(7):
        dates.append(date + datetime.timedelta(days=i))
    df = pd.DataFrame(dates, columns=['date'])
    X = get_features(df, 'date')
    recipe_df = pd.read_csv('models/recipe.csv')
    food_item_qty = {}
    food_items = recipe_df[recipe_df['ingredient_id']==ingredient_id]['food_item_id'].unique().tolist()
    qty_needed = np.array([0]*7).reshape(1,7)
    for food_item in food_items:
        rf = pickle.load(open(f'models/{food_item}.pkl','rb'))
        preds = rf.predict(X)
        qty = recipe_df[(recipe_df['ingredient_id']==ingredient_id) & 
                        (recipe_df['food_item_id']==food_item)]['ingredient_quantity'].values[0]
        qty_needed = np.concatenate([qty_needed, preds*qty])
    return list(np.sum(qty_needed, axis=0))