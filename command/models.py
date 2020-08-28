from django.db import models
from django.db.models import Sum, Count
from product.models import Product
from django.contrib.auth.models import User
from django.utils import timezone


class Table(models.Model):
    """ Table """
    TABLE_STATUS = [
        ('open', 'Ouverte'),
        ('closed', 'Fermée'),
        ('taken', 'Prise'),
    ]
    number = models.IntegerField(primary_key=True, null=False, unique=True)
    size = models.IntegerField(null=False)
    status = models.CharField(max_length=50, choices=TABLE_STATUS, default='open')
    code = models.CharField(max_length=5, default='0000')

    class Meta:
        ordering = ['number']

    def __str__(self): 
        return ("Table: {} - {} - Code: {}".format(
            str(self.number),
            str(self.status),
            str(self.code),
            )
        )


class TableConnect(models.Model):
    """ Manage table connections 
        the code will be used for multiple connections """
    STATUS = [
        ('on', 'Active'),
        ('off', 'Inactive'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status =  models.CharField(max_length=50, choices=STATUS, default='on')

    def __str__(self):
        return ("{} - Table: {} - {}".format(
            str(self.user),
            str(self.table.number),
            str(self.status),
            )
        )


class TableConnectManager(models.Model):

    def get_connection_table(self, user):

        connection = TableConnect.objects.get(user=user, status='on')
        table_number = connection.table.number
        return table_number


class Bill(models.Model):
    """ Bill """
    BILL_STATUS = [
        ('open', 'En cours'),
        ('closed', 'Payée'),
    ]
    status = models.CharField(max_length=50, choices=BILL_STATUS, default='open')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return ("Table: {} - Réf: {} - Status: {}".format(
            str(self.table.number),
            str(self.id),
            str(self.status),
            )
        )


class BillManager(models.Model):

    def get_bill(self, table, status):

        bill = Bill.objects.get(table=table, status=status)
        return bill

    def amount_update(self, bill, amount):

        new_amount = Bill.objects.get(pk=bill)
        new_amount.amount += amount
        new_amount.save()


class Command(models.Model):
    """ Command """
    COMMAND_STATUS = [
        ('new', 'Nouvelle'),
        ('in progress', 'en cours'),
        ('delivered', 'Livrée'),
        ('payed', 'Payée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    status = models.CharField(max_length=50, choices=COMMAND_STATUS, default='new')
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return ("Table {} réf: {} - {} - {}".format(
            str(self.bill.table.number),
            str(self.bill.pk),
            str(self.product.name),
            str(self.status)
            )
        )


class CommandManager(models.Model):

    def new_order(self, user, bill, product, qty=None):

        new = Command.objects.create(
            user=user,
            bill=bill,
            product=product,
            price=product.unit_price)
        new.save()

        BillManager().amount_update(bill=bill.id, amount=new.price)
        return new

    def del_order(self, order_id):

        to_cancel = Command.objects.get(id=order_id, status='new')

        BillManager().amount_update(bill=to_cancel.bill.id, amount=-to_cancel.price)

        to_cancel.delete()

        return to_cancel.product

    def order_data(self, bill, status=None, user=None):
        
        if status:
            if user:
                items = Command.objects.filter(user=user, bill=bill).exclude(status='payed').exclude(status='delivered')
            else:
                items = Command.objects.filter(bill=bill, status=status).exclude(status='payed').exclude(status='delivered')
        else:
            if user:
                items = Command.objects.filter(user=user, bill=bill).exclude(status='new').exclude(status='in progress')
            else:
                items = Command.objects.filter(bill=bill).exclude(status='new').exclude(status='in progress')
        
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

        
class Payment(models.Model):
    """ Payment """
    MODE = [
        ('cb', 'Carte bleue'),
        ('cash', 'liquide'),
        ('tr', 'Ticket restaurant'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.FloatField()
    mode = models.CharField(max_length=50, choices=MODE)
    date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        
        return ("{} - {} - {} - {}".format(
            str(self.bill.pk),
            str(self.user),
            str(self.amount),
            str(self.mode)
            )
        ) 


class PaymentManager(models.Model):
    
    def payment(self, bill, user=None):
        if user:
            try:
                new = Command.objects.filter(user=user, bill=bill, status='new')
                new.delete()
                to_pay = Command.objects.filter(user=user, bill=bill).exclude(status='').exclude(status='payed')
            except:
                print('hein?')

        else:
            try:
                new = Command.objects.filter(bill=bill, status='new')
                new.delete()
                to_pay = Command.objects.filter(bill=bill).exclude(status='').exclude(status='payed')
            except:
                print('hein?')
        
        to_pay.update(status='payed')
