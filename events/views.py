from django.shortcuts import render
from events.services.EventService import EventService


def home_page(request):
    events = EventService.events()

    return render(request, 'home.html', {
        'events': events['response']['events'],
    })


def events_page(request, month, day):
    events = EventService.events(month, day)

    return render(request, 'home.html', {
        'events': events['response']['events'],
    })
