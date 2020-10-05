from django.test import TestCase, Client
from django.urls import resolve, reverse

class TestUrls(TestCase):

    def test_new_comment(self):
        resolver_match = resolve('/message/add')
        self.assertEqual(
            resolver_match.func.__name__,
            'new_comment'
            )
    
    def test_check_comment(self):
        resolver_match = resolve('/message/check')
        self.assertEqual(
            resolver_match.func.__name__,
            'check_comment'
            )