from django.shortcuts import render, get_object_or_404
from pro.models import Invoice, Offer, Event, EventDetail


def index(request):
    next_events = Event.objects.all().order_by('date_from')[:3]
    return render(request, 'index.html', {'next_events':next_events})


def more(request, pk):
    # event = Event.objects.get(pk=pk)
    event = get_object_or_404(Event, id=pk)
    description = event.description

    return render(request, 'more.html', {'event_name': event, 'title': event, 'description': description})

def tickets(request, pk):
    event = get_object_or_404(Event, id=pk)
    return render(request, 'tickets.html', {'event_name': event})