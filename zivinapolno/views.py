import datetime

from django.shortcuts import render, get_object_or_404, redirect

from pro.admin import admin_mail
from pro.models import Invoice, Offer, Event, EventDetail, Product, ProductEvent, ProductQuantity, Activity, SubActivity
from utils.costumer_related import mail, create_offer
from .forms import RegistrationForm, LoginForm, TicketForm
from random import choice
from string import ascii_letters, digits


def index(request):
    next_events = Event.objects.all().order_by('date_from')[:3]
    all_activities = Activity.objects.all().order_by('z_index')

    return render(request, 'index.html', {'next_events': next_events, 'all_activities': all_activities})


def more(request, pk):

    if request.method == "POST":
        offer = create_offer(request.user, request.POST)
        mail(offer)

        return render(request, 'bought_tickets.html', {'adress': request.user.email})

    else:
        event = get_object_or_404(Event, id=pk)
        description = event.description
        event_detail = EventDetail.objects.filter(event=event)
        products = ProductEvent.objects.filter(event_detail=event_detail)

        return render(request, 'more.html', {
                                                'event_name': event,
                                                'description': description,
                                                'products': products,
                                            })


def tickets(request, pk):

    if request.method == "POST":
        offer = create_offer(request.user, request.POST)
        mail(offer)

        return render(request, 'bought_tickets.html', {'adress': request.user.email})

    else:
        event = get_object_or_404(Event, id=pk)
        event_detail = EventDetail.objects.filter(event=event)
        products = ProductEvent.objects.filter(event_detail=event_detail)

        return render(request, 'tickets.html', {
                                                'event_name': event,
                                                'products': products,
                                            })


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


def about(request, pk):

    activity = get_object_or_404(Activity, pk=pk)
    description = activity.description
    sub_activities = SubActivity.objects.filter(activity=activity)

    return render(request, 'about.html', {
                                            'activity': activity,
                                            'description': description,
                                            'sub_activities': sub_activities,
                                        })