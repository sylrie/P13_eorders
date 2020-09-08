from .models import *

class TableConnectManager(models.Model):

    def get_connection_table(self, user):

        connection = TableConnect.objects.get(user=user, status='on')
        table_number = connection.table.number
        return table_number
        
    def get_customers(self, table, action=None):

        customers = TableConnect.objects.filter(table=table, status='on')
        
        if action:
            for user in customers:
                user = customers.get(user=user.user)
                user.status = action
                user.save()

        return customers

    def close_connection_table(self, table, user=None):
        if user:
            to_close = TableConnect.objects.filter(table=table, user=user, status='on')
            
        else:
            to_close = TableConnect.objects.filter(table=table, status='on')
        
        try:
            for connection in to_close:
                connection.status = 'off'
                connection.save()
        except:
        
            to_close.status = 'off'
            to_close.save()
   

class BillManager(models.Model):

    def get_bill(self, table, status):

        bill = Bill.objects.get(table=table, status=status)
        return bill

    def amount_update(self, bill, amount):

        new_amount = Bill.objects.get(pk=bill)
        new_amount.amount += amount
        new_amount.save()

    def close_bill(self, bill):
        try:
            to_close = Bill.objects.get(pk=bill.id)
            to_close.status = 'closed'
            to_close.save()
        except Exception as e:
            print(e)


class CommandManager(models.Model):

    def new_order(self, user, bill, product, qty=None):
      
        new = Command.objects.create(
            user=user,
            bill=bill,
            product=product,
            price=product.unit_price
            )
        new.save()
        
        return new

    def del_order(self, order_id):

        to_cancel = Command.objects.get(id=order_id, status='new')
        
        BillManager().amount_update(bill=to_cancel.bill.id, amount=-to_cancel.price)

        to_cancel.delete()
        return to_cancel.product
       
    def add_bill(self, user, bill, name):
        
        try:
            old_user = User.objects.get(username=name.lower())
            to_change = Command.objects.filter(bill=bill, user=old_user)
            
            to_change.update(user=user)
            connection = TableConnect.objects.get(user=old_user, status='on')
            connection.status = 'off'
            connection.save()
        except Exception as e:
            print(e)

    def order_data(self, bill, status=None, user=None):
        
        if status:
            if user:
                items = Command.objects.filter(user=user, bill=bill).exclude(status='payed').exclude(status='delivered')
            else:
                items = Command.objects.filter(bill=bill).exclude(status='payed').exclude(status='delivered')
        else:
            if user:
                items = Command.objects.filter(user=user, bill=bill).exclude(status='new').exclude(status='in-progress')
            else:
                items = Command.objects.filter(bill=bill).exclude(status='new').exclude(status='in-progress')
        
        items_qty = items.exclude(status='payed').aggregate(Count('status'))
        total_price = 0
        for item in items.exclude(status='payed'):
            total_price += item.price 
        
        order = {
            'items_qty': items_qty['status__count'],
            'total_price': total_price
        }
        return order

    def get_bill_data(self, bill, user=None):

        if user:
            orders = Command.objects.filter(user=user, bill=bill).order_by('status', 'product')
        else:
            orders = Command.objects.filter(bill=bill).order_by('status', 'product')#.distinct('status', 'product')
        
        return orders

    def get_amount(self, bill):

        orders = Command.objects.filter(bill=bill)
        amount = orders.aggregate(Sum('price'))

        return amount['price__sum']

    def update_status(self, order_id, status):
        try:
            order = Command.objects.get(pk=order_id)
            order.status = status
            order.save()
        except Exception as e:
            print(e)


class CallManager(models.Model):

    def new_call(self, table, name):
        call_name = StaffCall.objects.get(name=name)
        call_table = Table.objects.get(pk=table)
        exist_call = Call.objects.filter(table=call_table, name=call_name)
        if not exist_call:
            new = Call.objects.create(
                table=call_table,
                name=call_name)
            new.save()

    def del_call(self, call_id):
        to_cancel = Call.objects.get(id=call_id)
        to_cancel.delete()

    def get_calls(self, table):
        call_table = Table.objects.get(pk=table)
        calls = Call.objects.filter(table=call_table, active=True)
        return calls

    def close_call(self, call):
        to_close = Call.objects.get(pk=call)
        to_close.active = False
        to_close.save()


class PaymentManager(models.Model):
    
    def get_payment(self, bill):

        payments = Payment.objects.filter(bill=bill)
        amount = payments.aggregate(Sum('amount'))

        return amount['amount__sum']

    def payment_bill(self, user, bill, amount):
        
        try:
            payment = Payment.objects.create(
            user=user,
            bill=bill,
            amount=amount
            )
            payment.save()
            return True
        except:
            return False

        
    def pay_orders(self, bill, user):
        
        try:

            to_change = Command.objects.filter(bill=bill, user=user).exclude(status='payed')
            
            for order in to_change:
                order.status = 'payed'
                
                order.save()
        except:
            pass


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
