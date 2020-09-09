from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .models import *
from .db_manager import *
from product.models import ProductManager
from .scripts import table_connection, closing_table
from .forms import JoinTable, PayBill
#from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request, error=None):
    """ Home page """
    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    if request.user.is_staff:
        return StaffManager().all_data(request)

    else:
        try:
            TableConnectManager().get_connection_table(user=request.user)
            return OrderManager().ordering(request)
        
        except:
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
    
    if not request.user.is_authenticated:
         return index(request)
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
        else:
            return index(request)
        
        if self.table:
            code = Table.objects.get(number=self.table)
            self.code = code.code
            self.bill = BillManager().get_bill(table=self.table, status='open')
        
        else:
            return index(request)
            
    def ordering(self, request):
        self.get_data(request)
        self.menu = ProductManager().get_menu()
        self.product = None
        self.order_id = None
        self.new_data = None
        self.family = None
        self.error = None
        self.calls = None

        if request.GET.get('add-product'):
           
            product = request.GET.get("add-product")
        
            self.product = ProductManager().get_product(product)
            
            try:

                self.order_id = CommandManager().new_order(user=self.user, bill=self.bill, product=self.product)         
                self.message = "+ {}".format(self.product.name)
                
            except:
                self.message = "Vous devez être connecté(e) à une table"
               
                return index(request, error=self.message)

        else:

            if request.GET.get('del-product'):
                self.order_id = request.GET.get('del-product')

            elif request.GET.get('del-product-bill'):
                self.order_id = request.GET.get('del-product-bill')
                
            if self.order_id:
                try:
                    self.product = CommandManager().del_order(order_id=self.order_id)
                    self.message = "- {}".format(
                        self.product.name
                    )
                    self.order_id = None
                except:
                    self.error = "La commande à déjà été prise en compte ou supprimée"
        
        if request.GET.get('del-product-bill'):
            return self.get_bill(request)
      
        else:
            
            self.new_data = CommandManager().order_data(user=self.user, bill=self.bill, status="new")
            
            self.calls = CallManager().get_calls(table=self.table)

            context = {
                'message': self.message,
                'error': self.error,
                'table': self.table,
                'code': self.code,
                'calls': self.calls,
                'bill': self.bill,
                'menu': self.menu,
                'order_id': self.order_id,
                'new_data': self.new_data,
                'family': self.family
            }
            
            return render(request, 'command/ordering.html', context)
    
    def calling(self,request):
        self.get_data(request)
        self.name =None

        if request.GET.get('call'):
            self.name = request.GET.get("call")

            try:
                CallManager().new_call(table=self.table, name=self.name)
                
            except Exception as e:
                print(e)
            
        if request.GET.get('del-call'):
            call_id = request.GET.get("del-call")
            try:
                CallManager().del_call(call_id=call_id)
            except Exception as e:
                print(e)
        
        if self.name == 'Régler la note':
            pass
        else:
            return redirect('ordering')

    def get_bill(self, request):
        self.get_data(request)
        self.filter_name = {
            "name": self.table,
            "filter": 'Table '
        }

        if request.GET.get('filter-name'):
            filter_name = request.GET.get('filter-name')

            user = User.objects.get(username=filter_name)
            self.bill_data =CommandManager().get_bill_data(user=user, bill=self.bill)
            self.new_data = CommandManager().order_data(user=user, bill=self.bill, status="new")
            self.order_data = CommandManager().order_data(user=user, bill=self.bill)
            self.filter_name = {
                "name": filter_name.capitalize(),
                "filter": 'Client  '
            }
            
        
        else:
            self.new_data = CommandManager().order_data(bill=self.bill, status="new")
            self.order_data = CommandManager().order_data(bill=self.bill)
            self.bill_data =CommandManager().get_bill_data(bill=self.bill)
        
        self.bill_amount = CommandManager().get_amount(bill=self.bill)

        context = {
            'bill_data': self.bill_data,
            'user':self.user,
            'order_data': self.order_data,
            'new_data': self.new_data,
            'filter_name': self.filter_name,
            'table': self.table,
            'code': self.code,
            'bill_amount': self.bill_amount,
        }   
        return render(request, 'command/bill.html', context)

    def check_bill(self, request):
        self.get_data(request)

        self.bill_amount = CommandManager().get_amount(bill=self.bill)
        if not self.bill_amount:
            return self.ordering(request)

        self.payed_amount = PaymentManager().get_payment(bill=self.bill)
        
        if self.payed_amount:
            self.rest_amount = self.bill_amount - self.payed_amount
        else:
            self.rest_amount = self.bill_amount

        self.bill_user = CommandManager().get_bill_data(user=self.user, bill=self.bill).exclude(status='payed').aggregate(Sum('price'))
        
        self.customers = TableConnectManager().get_customers(table=self.table)
        self.nbr_user = len(self.customers)
        
        self.split_bill = self.bill_amount/self.nbr_user
      

        context = {
            'user':self.user,
            'bill_amount': self.bill_amount,
            'payed_amount': self.payed_amount,
            'rest_amount': self.rest_amount,
            'bill_user': self.bill_user['price__sum'],
            'customers': self.customers,
            'nbr_user': self.nbr_user,
            'split_bill': self.split_bill,
        }

        return render(request, 'command/check_bill.html', context)

    def pay_bill(self, request): 
        self.get_data(request)
        self.bill_amount = CommandManager().get_amount(bill=self.bill)
        self.error = None
        payed = False
        try:
            if request.GET.get('add-bill'):
                name = request.GET.get('add-bill')
                CommandManager().add_bill(user=self.user, bill=self.bill, name=name)
                return self.check_bill(request)

            elif request.GET.get('total-amount'):
                
                amount = CommandManager().get_amount(bill=self.bill)
                if amount:
                    payed = PaymentManager().payment_bill(user=self.user, bill=self.bill, amount=amount)
                    if payed:

                        TableConnectManager().close_connection_table(table=self.table)
                else:
                    redirect('index')
            
            elif request.GET.get('user-amount'):
                
                self.bill_user = CommandManager().get_bill_data(user=self.user, bill=self.bill).aggregate(Sum('price'))
                amount =  self.bill_user['price__sum']

                payed = PaymentManager().payment_bill(user=self.user, bill=self.bill, amount=amount)

                if payed:
                    PaymentManager().pay_orders(user=self.user, bill=self.bill)
                    TableConnectManager().close_connection_table(table=self.table, user=self.user)

            elif request.GET.get('split-amount'):
                self.customers = TableConnectManager().get_customers(table=self.table)
                self.nbr_user = len(self.customers)
                amount = self.bill_amount/self.nbr_user
                

                payed = PaymentManager().payment_bill(user=self.user, bill=self.bill, amount=amount)
                if payed:
                    TableConnectManager().close_connection_table(table=self.table, user=self.user)
       
        except:
            self.error = "oups une erreur s'est produite"
        
        if payed:
            self.bill_amount = CommandManager().get_amount(bill=self.bill)
            self.payed_amount = PaymentManager().get_payment(bill=self.bill)
            
            if self.payed_amount:
                self.rest_amount = self.bill_amount - self.payed_amount
            
                if self.rest_amount <= 0:
                    
                    BillManager().close_bill(bill=self.bill)

                    to_close = Table.objects.get(pk=self.table)
                    to_close.status = "open"
                    to_close.save()

            
        context = {
            'user': self.user,
            'amount': amount,
            'error': self.error,
        }
        return render(request, 'command/payment.html', context)
            

class StaffManager():

    def all_data(self, request):
        
        if request.user.is_staff:
            open_bills = Bill.objects.filter(status='open')
            calls = Call.objects.filter(active=True)
            
            orders = Command.objects.all().exclude(status='payed').exclude(status=('delivered')).order_by('-status')
            context = {
                'orders': orders,
                'bills': open_bills,
                'calls': calls
            }
            return render(request, 'command/staff.html', context)

        else:
            return index(request)

    def change_status(self, request):
        
        if request.user.is_staff:
            if request.GET.get('close-call'):
                call = request.GET.get('close-call')
                try:
                    CallManager().close_call(call=call)
                except Exception as e:
                    print(e)
            else:
                if request.GET.get('in-progress'):
                    order = request.GET.get('in-progress')
                    status = 'in-progress'
                if request.GET.get('delivered'):
                    order = request.GET.get('delivered')
                    status = 'delivered'
            
                CommandManager().update_status(order_id=order, status=status)
                
            return self.all_data(request)
    
        else:
            return index(request)

    def pay_by_staff(self,request):

        if request.user.is_staff:
            bill_id = int(request.GET.get('bill'))

            bill = Bill.objects.get(pk=bill_id)
            amount = CommandManager().get_amount(bill=bill)

            PaymentManager().payment_bill(user=request.user, bill=bill, amount=amount)
            
            
            table = bill.table.number
            TableConnectManager().close_connection_table(table=table)
            
            to_open =  Table.objects.get(pk=table)
            to_open.status = 'open'
            to_open.save()
            
            BillManager().close_bill(bill=bill)

            return self.all_data(request)
        
        else:
            return index(request)