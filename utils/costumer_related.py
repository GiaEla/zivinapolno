from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from pro.models import Offer, Invoice


def mail(queryset):

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
