from django.db import models

from pro.models import ProductQuantityInvoice, ProductQuantityOffer, Product, Vat
from utils.generators import generate_pdf


class InvoiceWrapper:

    @staticmethod
    def generate_invoice(invoice_obj):
        products_quantity = ProductQuantityInvoice.objects.filter(invoice=invoice_obj.id)
        product_with_prices = []

        for quantity in products_quantity:
            product = Product.objects.get(id=quantity.product.id)
            price_no_vat = product.price_no_vat * quantity.qt_value
            price_with_vat = product.price_with_vat * quantity.qt_value
            vat = Vat.objects.get(id=product.vat_id).value
            product_with_prices.append({'name': product.name,
                           'quantity': quantity.qt_value,
                           'price_no_vat': price_no_vat,
                           'vat': vat,
                           'price_with_vat': price_with_vat, })

        html_context = {
            'products': product_with_prices,
            'invoice_number': invoice_obj.invoice_number,
        }

        pdf_path = generate_pdf('invoice.html', html_context, 'invoices', str(invoice_obj.invoice_number) + '.pdf')

        return pdf_path


class OfferWrapper:

    @staticmethod
    def generate_offer(offer_obj):
        products_quantity = ProductQuantityOffer.objects.filter(invoice=offer_obj.id)
        product_with_prices = []

        for quantity in products_quantity:
            product = Product.objects.get(id=quantity.product.id)
            price_no_vat = product.price_no_vat * quantity.qt_value
            price_with_vat = product.price_with_vat * quantity.qt_value
            vat = Vat.objects.get(id=product.vat_id).value
            product_with_prices.append({
                'name': product.name,
                'quantity': quantity.qt_value,
                'price_no_vat': price_no_vat,
                'vat': vat,
                'price_with_vat': price_with_vat, })

        html_context = {
            'products': product_with_prices,
            'invoice_number': offer_obj.invoice_number,
        }

        pdf_path = generate_pdf('offer.html', html_context, 'offers', str(offer_obj.offer_number) + '.pdf')

        return pdf_path

