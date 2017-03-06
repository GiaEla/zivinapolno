from decimal import *


def generate_object_number(date, last_object, type):
    """
    generates number for invoices and offers in form - last two numbers of a year + serial number
    :param date: date of invoice or offer
    :param last_object: last created object in current year
    :param type: invoice or offer
    :return: generated invoice or offer number
    """

    if not last_object:
        generated_number = date.year + '0000'

    elif type == "offer":
        generated_number = last_object.offer_number + 1

    elif type == "invoice":
        generated_number = last_object.invoice_number + 1

    else:
        generated_number = 0

    return generated_number


def generate_price_with_vat(price_no_vat, vat):
    """
    generates price with vat
    :param price_no_vat: price without vat
    :param vat: vat rate
    :return: price with vat
    """

    price_float = price_no_vat * (Decimal('1') + vat/Decimal('100'))
    price = Decimal(str(price_float)).quantize(Decimal('.01'), rounding=ROUND_DOWN)

    return price

