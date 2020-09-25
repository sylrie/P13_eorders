from django.db import models
from django.db.models import Sum, Count
from product.models import Product, StaffCall
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

class Bill(models.Model):
    """ Bill """
    BILL_STATUS = [
        ('open', 'En cours'),
        ('closed', 'Payée'),
    ]
    status = models.CharField(max_length=50, choices=BILL_STATUS, default='open')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
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

class Command(models.Model):
    """ Command """
    COMMAND_STATUS = [
        ('new', 'Nouvelle'),
        ('in-progress', 'en cours'),
        ('delivered', 'Livrée'),
        ('payed', 'Payée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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

class Call(models.Model):
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.ForeignKey(StaffCall, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ("Table {} - {} - {}".format(
            str(self.table.number),
            str(self.name),
            str(self.active)
            )
        )

class Payment(models.Model):
    """ Payment """
    MODE = [
        ('cb', 'Carte bleue'),
        ('cash', 'liquide'),
        ('tr', 'Ticket restaurant'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(max_length=50, choices=MODE, null=True)
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

class Tips(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)        