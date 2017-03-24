from django.shortcuts import render
from wrapps.invoice_wrapper import InvoiceWrapper
from pro.models import Invoice


def index(request):
    last_object = Invoice.objects.all().order_by('date').last()
    InvoiceWrapper.generate_invoice(last_object)
    return render(request, 'index.html')


