from django.shortcuts import render, redirect

from .models import Table, TableConnect, Bill, TableConnectManager, BillManager, CommandManager
from product.models import ProductManager
from .scripts import table_connection, closing_table
from .forms import JoinTable
#from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request, error=None):
    """ Home page """
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')

    else:
        open_table = Table.objects.filter(status='open')
        taken_table = Table.objects.filter(status='taken')
        
        message = "Sélectionnez la table"
        context = {
            'error': error,
            'open_table': open_table,
            'taken_table': taken_table,
            'message': message,
        }
        return render(request, 'command/home.html', context)

def openning_bill(request):

    if request.method == 'POST':
        form = JoinTable(request.POST)
        if form.is_valid():
            table = form.cleaned_data['table']
            code = form.cleaned_data['code']
            secret_code = Table.objects.get(number=int(table))
            
            if secret_code.code == code:
                
                new_connection = table_connection(table=table, user=request.user)
                
            else:
                message = "Mauvais code"
                return index(request, error=message)
        else:
            pass
            
    else: 
        table = request.GET.get("table")
        check_table = Table.objects.filter(number=table, status='taken')

        if check_table:
            check_connection = TableConnectManager().get_connection_table(user=request.user)
            if not check_connection:

                message = "Oups, la table {} est déjà prise".format(table)
                return index(request, error=message)

        new_connection = table_connection(table=table, user=request.user, new=True)
        code = new_connection
    
    return OrderManager().ordering(request)

def closing_bill(request):
    table = request.GET.get("table")
    to_close = closing_table(table=table)
    return redirect('index')


class OrderManager():

    def get_data(self, request):
        self.user = request.user
        self.table = None
        self.code = None
        self.bill = None
        self.message = None
        
        if self.user:
            try:
                self.table = TableConnectManager().get_connection_table(user=self.user)
            except:
                pass

        if self.table:
            code = Table.objects.get(number=self.table)
            self.code = code.code
            try:
                self.bill = BillManager().get_bill(table=self.table, status='open')
            except:
                pass


        return index(request)
    
    def ordering(self, request):
        self.get_data(request)
        self.menu = ProductManager().get_menu()
        self.product = None
        self.order_id = None
        self.order_data = None
        self.family = None
        
        if request.GET.get('family'):
            print('ok')
            self.family = request.GET.get('family')
            self.menu = ProductManager().get_menu(family_name=self.family)

        if request.GET.get('add-product'):
            product = request.GET.get("add-product")
        
            self.product = ProductManager().get_product(product)
            
            try:

                self.order_id = CommandManager().new_order(user=self.user, bill=self.bill, product=self.product)         
                self.message = "+ {}".format(self.product.name)
                
            except Exception as err:
                print(err)
                self.message = "Oups, la commande n'est pas passée ^^"
               
                return index(request, error=self.message)

        elif request.GET.get('del-product'):
            order_id = request.GET.get('del-product')

            try:

                self.product = CommandManager().del_order(order_id=order_id)
                self.message = "- {}".format(
                    self.product.name
                )
            except Exception as err:
                print(err)

        self.order_data = CommandManager().new_order_data(user=self.user, bill=self.bill)
        #self.items_data = items_data.items_qty
        context = {
            'message': self.message,
            'table': self.table,
            'code': self.code,
            'bill': self.bill,
            'menu': self.menu,
            'order_id': self.order_id,
            'order_data': self.order_data,
            'family': self.family
        }
        
        return render(request, 'command/ordering.html', context)
    
    def get_bill(self, request):
        self.get_data(request)
        self.bill_data =CommandManager().get_bill_data(bill=self.bill)
        context = {
            'bill_data': self.bill_data,
            'user':self.user
        }   
        return render(request, 'command/bill.html', context)
