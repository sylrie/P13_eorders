""" urls for user app """
from django.urls import path
from . import views

APP_NAME = 'product'

urlpatterns = [
    path('product/menu/', views.menu, name='menu'),
]