from django.shortcuts import render, get_object_or_404, redirect
from pro.models import Invoice, Offer, Event, EventDetail
from .forms import RegistrationForm, LoginForm
from random import choice
from string import ascii_letters, digits


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
            return redirect('success.html')

    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})
