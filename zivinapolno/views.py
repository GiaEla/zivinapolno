import datetime

from django.shortcuts import render, get_object_or_404, redirect

from pro.admin import admin_mail
from pro.models import Invoice, Offer, Event, EventDetail, Product, ProductEvent, ProductQuantity, Activity
from utils.costumer_related import mail
from .forms import RegistrationForm, LoginForm, TicketForm
from random import choice
from string import ascii_letters, digits


def index(request):
    next_events = Event.objects.all().order_by('date_from')[:3]
    all_activities = Activity.objects.all().order_by('z_index')

    return render(request, 'index.html', {'next_events': next_events, 'all_activities': all_activities})


def more(request, pk):

    if request.method == "POST":
        offer = Offer()
        offer.date = datetime.datetime.now()
        offer.place = "Center Živi na polno, Ljubljana"
        offer.recipient = request.user
        offer.payed = False
        offer.save()

        adress = request.user.email
        ordered = request.POST

        for key, value in ordered.items():
            if key == 'csrfmiddlewaretoken':
                continue
            else:
                product_quantity = ProductQuantity()
                product_quantity.product_event = ProductEvent.objects.get(id=int(key))
                product_quantity.offer = offer
                product_quantity.qt_value = int(value)
                product_quantity.product = None
                product_quantity.save()

        mail(offer)

        return render(request, 'bought_tickets.html', {'adress': adress})

    else:
        event = get_object_or_404(Event, id=pk)
        description = event.description
        event_detail = EventDetail.objects.filter(event=event)
        products = ProductEvent.objects.filter(event_detail=event_detail)
        # quantities = ProductQuantity(product_event= products, qt_value= 0)

        return render(request, 'more.html', {
                                                'event_name': event,
                                                'description': description,
                                                'products': products,
                                            })


def tickets(request, pk):
    event = get_object_or_404(Event, id=pk)
    return render(request, 'tickets.html', {'event_name': event})


def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.token = ''. join(choice(ascii_letters + digits) for i in range(15))
            registration.save()
            return redirect('success')

    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def login(request):
    form = LoginForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            return redirect('index.html')
        else:
            return redirect('error.html')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

