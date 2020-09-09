import random
from .models import *
from product.models import ProductManager


def table_connection(table, user, new=False):
    """ Manage connections to tables """
    
    # Get table
    table = Table.objects.get(number=int(table))
    
    #Connection table
    connection = TableConnect.objects.filter(user=user, status='on')
    if not connection:
        new_connection = TableConnect.objects.create(
            table=table,
            user=user,
        )
        new_connection.save()
    
        if new:
            # Openning bill
            bill = Bill.objects.create(
                table=table,
            )
            bill.save()
            # Change status table
            table.status = 'taken'
            # Create secret code
            code = str(random.randint(0000,9999))
            table.code = code
            table.save()

            return code
    else:
        
        pass

