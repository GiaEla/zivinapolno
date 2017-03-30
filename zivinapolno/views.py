from django.shortcuts import render
from wrapps.invoice_wrapper import InvoiceWrapper, OfferWrapper
from pro.models import Invoice, Offer


def index(request):
    last_object = Offer.objects.all().order_by('date').last()
    OfferWrapper.generate_offer(last_object)
    return render(request, 'index.html')


