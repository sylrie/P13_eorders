from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.db.models.query import QuerySet


class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        
    def test_menu(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/menu.html')
