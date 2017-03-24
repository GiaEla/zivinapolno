from decimal import Decimal
from django.test import TestCase
from utils.generators import generate_price_with_vat, generate_pdf


class TestGenerators(TestCase):

    def setUp(self):
        self.price_no_vat = Decimal('100.00')
        self.vat = Decimal('22.5')

    def test_generate_price_with_vat(self):
        price_with_vat = generate_price_with_vat(self.price_no_vat, self.vat)
        self.assertEqual(price_with_vat, Decimal('122.5'))

    def test_generate_pdf(self):
        pdf_test = generate_pdf()
        print(pdf_test)
