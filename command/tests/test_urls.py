from django.test import TestCase, Client
from django.urls import resolve, reverse

class TestUrls(TestCase):

    def test_get_bill_url(self):
        resolver_match = resolve('/command/get_bill')
        self.assertEqual(
            resolver_match.func.__name__,
            'get_bill'
            )
    
    def test_check_bill_url(self):
        resolver_match = resolve('/command/check_bill')
        self.assertEqual(
            resolver_match.func.__name__,
            'check_bill'
            )

    def test_tip_bill_url(self):
        resolver_match = resolve('/command/tip_bill')
        self.assertEqual(
            resolver_match.func.__name__,
            'tip_bill'
            )

    def test_pay_bill_url(self):
        resolver_match = resolve('/command/pay_bill')
        self.assertEqual(
            resolver_match.func.__name__,
            'pay_bill'
            )
    
    def test_openning_bill_url(self):
        resolver_match = resolve('/command/open_bill')
        self.assertEqual(
            resolver_match.func.__name__,
            'openning_bill'
            )
    
    def test_ordering_url(self):
        resolver_match = resolve('/command/ordering')
        self.assertEqual(
            resolver_match.func.__name__,
            'ordering'
            )
    
    def test_calling_url(self):
        resolver_match = resolve('/command/calling')
        self.assertEqual(
            resolver_match.func.__name__,
            'calling'
            )
    
    def test_change_status_url(self):
        resolver_match = resolve('/command/change_status')
        self.assertEqual(
            resolver_match.func.__name__,
            'change_status'
            )
    
    def test_pay_by_staff_url(self):
        resolver_match = resolve('/command/pay_by_staff')
        self.assertEqual(
            resolver_match.func.__name__,
            'pay_by_staff'
            )
    
    