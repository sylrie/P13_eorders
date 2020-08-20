from django.db import models
from django.db.models import Sum, Count
from pg_utils import DistinctSum
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
    code = models.CharField(max_length=5, default='00000')

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

class Command(models.Model):
    """ Command """
    COMMAND_STATUS = [
        ('new', 'Nouvelle'),
        ('delivered', 'Livrée'),
        ('canceled', 'Annulée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
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

        return new

    def new_order_data(self, user, bill):

        items = Command.objects.filter(user=user, bill=bill, status='new')
        items_qty = items.aggregate(Count('status'))
        total_price = 0
        for item in items:
            total_price += item.price 
        
        order = {
            'items_qty': items_qty['status__count'],
            'total_price': total_price
        }
        return order

    def del_order(self, order_id):

        to_cancel = Command.objects.get(id=order_id)
        to_cancel.delete()
        return to_cancel.product
    
    def get_bill_data(self, bill, filter=None):
        #orders = orders.values('product').annotate(total=DistinctSum('qty'))
        #orders = Command.objects.filter(bill=bill).annotate(total_qty=Count('product')).order_by('-status', 'product')
        #orders = Command.objects.filter(bill=bill).order_by('-status', 'product', 'qty').annotate(total=('qty'))
        
        orders = Command.objects.filter(bill=bill).order_by('-status', 'product')#.distinct('status', 'product')
        
        return orders

