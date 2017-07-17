import datetime

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from pro.models import Offer, Invoice, ProductQuantity, ProductEvent
from utils.tokens import account_activation_token


def create_offer(user, product_quantities):
        offer = Offer()
        offer.date = datetime.datetime.now()
        offer.place = "Center Živi na polno, Ljubljana"
        offer.recipient = user
        offer.payed = False
        offer.save()

        for key, value in product_quantities.items():
            if key == 'csrfmiddlewaretoken':
                continue
            elif value == "0":
                continue
            else:
                product_quantity = ProductQuantity()
                product_quantity.product_event = ProductEvent.objects.get(id=int(key))
                product_quantity.offer = offer
                product_quantity.qt_value = int(value)
                product_quantity.product = None
                product_quantity.save()

        return offer


def mail(queryset):
    """ Sends mail with attachment (offer or invoice) users email"""

    subject = ''
    message = ''
    pdf_path = ''

    if isinstance(queryset, Offer):
            queryset.generate_pdf()
            html_context = {
                'recipient': queryset.recipient,
                'type': 'predračun',
                'date': queryset.date.date()
            }

            subject = 'Predračun št.' + str(queryset.offer_number)
            message = render_to_string('mail/pdf_offer_invoice.html', html_context)
            recipient_mail = queryset.recipient.email
            pdf_path = settings.STATICFILES_DIRS[0] + '\\pdfs\\offers\\' + str(queryset.offer_number) + '.pdf'

    elif isinstance(queryset, Invoice):
        queryset.generate_pdf()
        html_context = {
            'recipient': queryset.offer.recipient,
            'type': 'račun',
            'date': queryset.date.date()
        }

        subject = 'Račun št.' + str(queryset.offer_number)
        message = render_to_string('mail/pdf_offer_invoice.html', html_context)
        recipient_mail = queryset.recipient.email
        pdf_path = settings.STATICFILES_DIRS[0] + '\\pdfs\\offers\\' + str(queryset.offer_number) + '.pdf'

    email = EmailMessage(
        subject,
        message,
        'giacotesting@gmail.com',
        [recipient_mail],
    )

    email.attach_file(pdf_path)
    email.content_subtype = 'html'
    email.send()


def activation_mail(user):
    """ Sends activation mail"""

    subject = ''
    message = ''

    activation_link = settings.SITE_URL + 'potrditev/' + user.token + '/'

    html_context = {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'activation_link': activation_link,
    }

    subject = 'Aktivacija za email' + str(user.email)
    message = render_to_string('registration/activate.html', html_context)
    user_mail = user.email

    email = EmailMessage(
        subject,
        message,
        'giacotesting@gmail.com',
        [user_mail],
    )

    email.content_subtype = 'html'
    email.send()