from django.shortcuts import render
from .models import ProductManager
from message.models import Comment
# Create your views here.

def menu(request):

    menu = ProductManager().get_menu()
    comments = Comment.objects.filter(visible=True)
    context = {
        'menu': menu,
        'comments': comments
    }
    return render(request, 'product/menu.html', context)