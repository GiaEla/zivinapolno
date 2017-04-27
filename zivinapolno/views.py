from django.shortcuts import render
from pro.models import Invoice, Offer, Event, EventDetail


def index(request):
    next_events = Event.objects.all().order_by('date_from')[:3]
    # next_event = Event.objects.all().order_by('date_from').last()
    # last_object = Invoice.objects.all().order_by('date').last[:3]
    # last_object.generate_pdf()
    return render(request, 'index.html', {'next_events':next_events})


