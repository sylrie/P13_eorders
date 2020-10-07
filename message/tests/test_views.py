from django.test import TestCase, Client
from django.urls import resolve, reverse

class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
