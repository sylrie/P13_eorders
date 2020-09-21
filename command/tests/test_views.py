from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from command.models import *
from product.models import *

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
    
        self.user1 = User.objects.create_user(
                username='user1',
                email='user1@user1.fr',
                password='password',
            )

        self.staff1 = User.objects.create_user(
                username='staff1',
                email='staff1@staff1.fr',
                password='password',
                is_staff= True
            )

        self.table = Table.objects.create(
            number=1,
            size=2,
        )
        
        self.category = ProductCategory.objects.create(
            name='categorie'
        )
        self.taxe = ProductTaxe.objects.create(
            name='taxe',
            value='0.2'
        )
        self.family = ProductFamily.objects.create(
            name='famille'
        )
        self.product = Product.objects.create(
            name='nom du produit',
            unit_price=2.2,
            category=self.category,
            family=self.family,
            taxe=self.taxe
        )
        self.call = StaffCall.objects.create(
            name='appel'
        )
        
    def test_homepage_no_user(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        
    def test_homepage_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/home.html')

    def test_openning_bill_no_user(self):
        response = self.client.get(reverse('openning_bill'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
    
    def test_openning_bill(self):
        self.client.force_login(self.user1)
        self.table.save()
        response = self.client.get(
            '/command/open_bill?table=1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/ordering.html')
    
    def test_customer_flow(self):
        """ test customer flow:
            -new order
            -get-bill
            -check-bill
            -del-order
            -pay-bill """

        self.product.save()
        self.table.save()
        
        #acces no user
        response = self.client.get(
            '/command/open_bill?table=1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
        
        #acces
        self.client.force_login(self.user1)
        response = self.client.get(
            '/command/open_bill?table=1'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/ordering.html')
        
        #new order
        response = self.client.get(reverse('ordering_add'), {'add-product': self.product.name})
        self.assertTemplateUsed(response, 'command/ordering.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "+ {}".format(self.product.name))
        
        #get_bill
        response = self.client.get(reverse('get_bill'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/bill.html')

        #chek_bill
        response = self.client.get(reverse('check_bill'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/check_bill.html')

        #del order
        response = self.client.get(reverse('ordering_del'), {'del-product': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/ordering.html')
        self.assertContains(response, "- {}".format(self.product.name))

        #del order already deleted
        response = self.client.get(reverse('ordering_del'), {'del-product': self.product.name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/ordering.html')
        self.assertContains(response, "La commande à déjà été prise en compte ou supprimée")

        #chek_bill empty
        response = self.client.get(reverse('check_bill'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/ordering.html')

    def test_all_data(self):
        response = self.client.get(reverse('all_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

        self.client.force_login(self.staff1)
        response = self.client.get(reverse('all_data'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/staff.html')
    
