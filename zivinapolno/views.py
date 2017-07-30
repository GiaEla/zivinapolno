import datetime

from django.shortcuts import render, get_object_or_404, redirect

from pro.admin import admin_mail
from pro.models import Invoice, Offer, Event, EventDetail, Product, ProductEvent, ProductQuantity, Activity, SubActivity, \
    BankAccount, Reference, UserProfile
from utils.costumer_related import mail, create_offer, activation_mail
from .forms import RegistrationForm, LoginForm, TicketForm
from random import choice
from string import ascii_letters, digits


def index(request):
    next_events = Event.objects.all().order_by('date_from')[:3]
    all_activities = Activity.objects.all().order_by('z_index')
    accounts = BankAccount.objects.all()
    references = Reference.objects.all()


    return render(request, 'index.html', {'next_events': next_events, 'all_activities': all_activities, 'accounts': accounts, 'references': references})


def more(request, pk):

    if request.method == "POST":
        offer = create_offer(request.user, request.POST)
        mail(offer)

        return render(request, 'bought_tickets.html', {'adress': request.user.email})

    else:
        event = get_object_or_404(Event, id=pk)
        event_detail = EventDetail.objects.filter(event=event)
        products = ProductEvent.objects.filter(event_detail=event_detail)

        return render(request, 'more.html', {
                                                'event': event,
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
            user = form.save(commit=False)
            user.activated = False
            user.token = ''. join(choice(ascii_letters + digits) for i in range(15))
            user.save()

            activation_mail(user)
            return redirect('success')

    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def success(request):
    return render(request, 'registration/confirmed.html')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = form.username

        if form.is_valid():
            return redirect('index.html')
        else:
            return redirect('error.html')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def about(request, pk):

    activity = get_object_or_404(Activity, pk=pk)
    sub_activities = SubActivity.objects.filter(activity=activity)

    return render(request, 'about.html', {
                                            'activity': activity,
                                            'sub_activities': sub_activities,
                                        })


def about_sub(request, fk, pk):

    activity = get_object_or_404(Activity, pk=fk)
    sub_activity = SubActivity.objects.get(pk=pk)

    return render(request, 'about_subactivity.html', {
                                            'sub_activity': sub_activity,
                                        })


def confirmation(request, token):
    user = UserProfile.objects.get(token=token)
    if user is True:
        user.activated = True
        return render(request, 'registration/confirmed.html')
    else:
        return render(request, 'index.html')