from django.shortcuts import render
from events.services.EventService import EventService
from datetime import datetime


def home_page(request):
    events = EventService.events()
    date = datetime.now()

    return render(request, 'home.html', {
        'events': events['response']['events'],
        'date': date,
    })


def events_page(request, month, day):
    events = EventService.events(month, day)
    date = datetime.strptime(
            '{} {}'.format(day, month), '%d %B')

    return render(request, 'home.html', {
        'events': events['response']['events'],
        'date': date,
    })
