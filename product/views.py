from django.shortcuts import render
from .models import Product, ProductManager
# Create your views here.

def menu(request):

    product = ProductManager().get_menu()
    menu = product[0]
    category = product[1]
    family = product[2]
    context = {
        'menu': menu,
        'category': category,
        'family': family
    }
    print(menu)
    return render(request, 'product/menu.html', context)