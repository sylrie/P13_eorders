""" urls for user app """
from django.urls import path
from . import views

APP_NAME = 'order'

urlpatterns = [
    path('', views.index, name='index'),
    path('command/open_bill', views.openning_bill, name='openning_bill'),
    path('command/close_bill', views.closing_bill, name='closing_bill'),
    #path('command/ordering', views.ordering, name='ordering'),
    path('command/ordering_add', views.OrderManager().ordering, name='ordering'),
    path('command/ordering_del', views.OrderManager().ordering, name='ordering'),
    path('command/get_bill', views.OrderManager().get_bill, name='get_bill'),
    path('command/pay_bill', views.OrderManager().pay_bill, name='pay_bill'),

]