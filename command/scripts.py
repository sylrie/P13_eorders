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

def table_deconnection(table):

    # Get table
    table = Table.objects.get(number=int(table))

    # Change connection status
    to_deconnect = TableConnect.objects.filter(table=table)
    to_deconnect.status = "off"

def closing_table(table):
    
    table = Table.objects.get(number=int(table))

    bill_to_close = Bill.objects.get(table=table, status='open')
    bill_to_close.status = 'closed'
    bill_to_close.save()

    # Change connection status
    to_deconnect = TableConnect.objects.filter(table=table,status='on')
    for connection in to_deconnect:
        connection = to_deconnect.get(user=connection.user)
        connection.status = "off"
        connection.save()
    
    table.status = 'open'
    table.save()

"""def ordering_product(user, productname):

    try:
        table = TableConnectManager().get_connection_table(user=user)
        print(table)

        bill = BillManager().get_bill(table=table, status='open')
        print(bill)

        product = ProductManager().get_product(productname)

        CommandManager().new_order(user=user, bill=bill, product=product)

        print("{} ajouté".format(
            productname
            )
        )
    except Exception as err:
        print("oups! {}".format(
            err
            )
        )"""