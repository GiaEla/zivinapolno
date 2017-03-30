from django.db import models

from pro.models import ProductQuantityInvoice, ProductQuantityOffer, Product, Vat, Invoice, Reference
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
            'place': invoice_obj.place,
            'date': invoice_obj.date.date(),
            'total_no_vat': invoice_obj.total_no_vat,
            'total_with_vat': invoice_obj.total_with_vat,
        }

        pdf_path = generate_pdf('invoice.html', html_context, 'invoices', str(invoice_obj.invoice_number) + '.pdf')

        return pdf_path


class OfferWrapper:

    @staticmethod
    def generate_offer(offer_obj):
        products_quantity = ProductQuantityOffer.objects.filter(offer=offer_obj.id)
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
            'offer_number': offer_obj.offer_number,
            'total_no_vat': offer_obj.total_no_vat,
            'total_with_vat': offer_obj.total_with_vat,
            'place': offer_obj.place,
            'date': offer_obj.date,
            'bank_account': offer_obj.bank_account.account,
            'reference': offer_obj.reference.reference,
        }

        pdf_path = generate_pdf('offer.html', html_context, 'offers', str(offer_obj.offer_number) + '.pdf')

        return pdf_path

