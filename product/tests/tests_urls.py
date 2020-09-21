from django.test import TestCase, Client
from django.urls import resolve, reverse

# Create your tests here.

class TestUrls(TestCase):

    def test_menu_url(self):
        resolver_match = resolve('/command/menu')
        self.assertEqual(
            resolver_match.func.__name__,
            'menu'
            )