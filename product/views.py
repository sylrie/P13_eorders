from django.shortcuts import render
from .models import Product, ProductManager
# Create your views here.

def menu(request):

    menu = ProductManager().get_menu()
    context = {
        'menu': menu
    }
    return render(request, 'product/menu.html', context)