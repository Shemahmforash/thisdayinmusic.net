from math import ceil

from django.shortcuts import render
from events.services.EventService import EventService
from datetime import datetime
from django.conf import settings


def home_page(request):
    page = _get_current_page(request)

    service = EventService(settings.API_BASE_ADDRESS)
    events = service.events(page=page)
    date = datetime.now()

    pagination = events['response']['pagination']

    return render(request, 'home.html', {
        'events': events['response']['events'],
        'date': date,
        'current_page': page,
        'pages': _page_range(pagination['total'])
    })


def events_page(request, month, day):
    page = _get_current_page(request)

    service = EventService(settings.API_BASE_ADDRESS)
    events = service.events(month, day, page)

    date = datetime.strptime(
        '{} {}'.format(day, month), '%d %B')

    pagination = events['response']['pagination']

    return render(request, 'home.html', {
        'events': events['response']['events'],
        'date': date,
        'current_page': page,
        'pages': _page_range(pagination['total'])
    })


def _get_current_page(request):
    return int(request.GET.get('page', 1))


def _page_range(total):
    return range(1, 1 + ceil(total / EventService.RESULTS_PER_PAGE))


