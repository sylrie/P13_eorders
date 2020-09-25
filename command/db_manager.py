from .models import *

class TableConnectManager(models.Model):
    """ Manage table connections """
    def get_connection_table(self, user):
        """ get the user connection active """ 
        connection = TableConnect.objects.get(user=user, status='on')
        table_number = connection.table.number
        return table_number
        
    def get_customers(self, table, action=None):
        """ get users at the table """
        customers = TableConnect.objects.filter(table=table, status='on')
        
        if action:
            for user in customers:
                user = customers.get(user=user.user)
                user.status = action
                user.save()

        return customers

    def close_connection_table(self, table, user=None):
        """ close user table connection or all connections  """
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
    """ Manage bills """
    def get_bill(self, table, status):
        """ get bill id """
        bill = Bill.objects.get(table=table, status=status)
        return bill

    def close_bill(self, bill):
        """ close the selected bill """
        try:
            to_close = Bill.objects.get(pk=bill.id)
            to_close.status = 'closed'
            to_close.save()
        except Exception as e:
            print(e)


class CommandManager(models.Model):
    """ Manage orders """
    def new_order(self, user, bill, product, qty=None):
        """ add a new order """
        new = Command.objects.create(
            user=user,
            bill=bill,
            product=product,
            price=product.unit_price
            )
        new.save()
        
        return new

    def del_order(self, order_id):
        """ cancel an order """
       
        to_cancel = Command.objects.get(id=order_id, status='new')     
        to_cancel.delete()
        
        return to_cancel.product
       
    def add_bill(self, user, bill, name):
        """ change user on orders """
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
        """ get qty and price """
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
        """ get bill orders """
        if user:
            orders = Command.objects.filter(user=user, bill=bill).order_by('status', 'product')
        else:
            orders = Command.objects.filter(bill=bill).order_by('status', 'product')#.distinct('status', 'product')
        
        return orders

    def get_amount(self, bill):
        """ get bill amount """
        orders = Command.objects.filter(bill=bill)
        amount = orders.aggregate(Sum('price'))

        return amount['price__sum']

    def update_status(self, order_id, status):
        """ change status orders """
        try:
            order = Command.objects.get(pk=order_id)
            order.status = status
            order.save()
        except Exception as e:
            print(e)
        

class TipsManager(models.Model):
    
    def new_tip(self, user, bill, tip):
        """ add a new tip """
        try:
            exist_tip = Tips.objects.get(user=user, bill=bill)
        
            exist_tip.amount = tip
            exist_tip.save()
        
        except:
            
            new = Tips.objects.create(
                user=user,
                bill=bill,
                amount=tip,
                )
            new.save()
            

    def get_tip_amount(self, bill):
        amount = Tips.objects.filter(bill=bill).aggregate(Sum('amount'))
        print(amount)
        return amount

class CallManager(models.Model):
    """ Manage calls """
    def new_call(self, table, name):
        """ add a call """
        call_name = StaffCall.objects.get(name=name)
        call_table = Table.objects.get(pk=table)
        exist_call = Call.objects.filter(table=call_table, name=call_name)
        if not exist_call:
            new = Call.objects.create(
                table=call_table,
                name=call_name)
            new.save()

    def del_call(self, call_id):
        """ cancel a call """
        to_cancel = Call.objects.get(id=call_id)
        to_cancel.delete()

    def get_calls(self, table):
        """ get table calls """
        call_table = Table.objects.get(pk=table)
        calls = Call.objects.filter(table=call_table, active=True)
        return calls

    def close_call(self, call):
        """ Close a call """
        to_close = Call.objects.get(pk=call)
        to_close.active = False
        to_close.save()


class PaymentManager(models.Model):
    """ Manage Payments """
    def get_payment(self, bill):
        """ Get bill payments amount """
        payments = Payment.objects.filter(bill=bill)
        amount = payments.aggregate(Sum('amount'))

        return amount['amount__sum']

    def payment_bill(self, user, bill, amount):
        """ add a payment """
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
        """ change order status to 'payed' """
        try:

            to_change = Command.objects.filter(bill=bill, user=user).exclude(status='payed')
            
            for order in to_change:
                order.status = 'payed'
                
                order.save()
        except:
            pass

