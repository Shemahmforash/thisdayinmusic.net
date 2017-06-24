from django.shortcuts import render
from events.services.EventService import EventService
from datetime import datetime


def home_page(request):
    page = get_current_page(request)

    events = EventService.events(page=page)
    date = datetime.now()

    return render(request, 'home.html', {
        'events': events['response']['events'],
        'date': date,
    })


def events_page(request, month, day):
    page = get_current_page(request)

    events = EventService.events(month, day, page)

    date = datetime.strptime(
        '{} {}'.format(day, month), '%d %B')

    return render(request, 'home.html', {
        'events': events['response']['events'],
        'date': date,
    })


def get_current_page(request):
    return int(request.GET.get('page', 1))
