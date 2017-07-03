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
        'events': _transform_api_response_to_model_list(events['response']['events']),
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
        'events': _transform_api_response_to_model_list(events['response']['events']),
        'date': date,
        'current_page': page,
        'pages': _page_range(pagination['total'])
    })


def playlist_page(request):
    date = datetime.now()

    service = EventService(settings.API_BASE_ADDRESS)
    playlist = service.playlist()

    tracks = playlist['response']['tracks']

    spotify_playlist = ",".join([track['spotifyId'].rsplit(':', 1)[1] for track in tracks])

    return render(request, 'playlist.html', {
        'date': date,
        'playlist': tracks,
        'spotify_playlist': spotify_playlist
    })


def about_page(request):
    return render(request, 'about.html')


def _get_current_page(request):
    return int(request.GET.get('page', 1))


def _page_range(total):
    return range(1, 1 + ceil(total / EventService.RESULTS_PER_PAGE))


def _transform_api_response_to_model_list(events):
    return [_api_event_to_event_model(event) for event in events]


def _api_event_to_event_model(event):
    # name = event["name"] if event["name"] else None

    return Event(event["date"], event["description"], event["type"])


class Event(object):
    TWITTER_MSG_LEN = 140
    TWITTER_HASH_TAG = "#thisdayinmusic"
    TWITTER_USER = "@today_in_music"

    def __init__(self, event_date, description, event_type="Event", name=None):
        self.event_date = event_date
        self.description = description
        self.type = event_type
        self.name = name

        self.twitter_message = self._set_message()

    def _set_message(self):
        message = '%s - %s' % (self.event_date, self.description)

        if len(message) + len(' ' + self.TWITTER_HASH_TAG) <= self.TWITTER_MSG_LEN:
            message = '%s %s' % (message, self.TWITTER_HASH_TAG)

        if len(message) + len(' via ' + self.TWITTER_USER) <= self.TWITTER_MSG_LEN:
            message = '%s via %s' % (message, self.TWITTER_USER)

        return message
