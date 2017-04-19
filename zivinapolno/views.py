from django.shortcuts import render
from pro.models import Invoice, Offer


def index(request):
    #pass
    last_object = Offer.objects.all().order_by('date').last()
    last_object.generate_pdf()
    return render(request, 'index.html')


