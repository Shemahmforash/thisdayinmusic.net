from math import ceil

from datetime import datetime
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from events.services.event_service import EventService
from events.services.spotify_service import SpotifyService
from thisdayinmusic.settings import SPOTIFY_OAUTH

PLAYLIST_DATE_FORMAT = '%A, %d %B %Y'


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

    date = _get_date_from_month_day_values(day, month)

    pagination = events['response']['pagination']

    return render(request, 'home.html', {
        'events': _transform_api_response_to_model_list(events['response']['events']),
        'date': date,
        'current_page': page,
        'pages': _page_range(pagination['total'])
    })


def playlist_page(request, month=None, day=None):
    date = _get_date_from_month_day_values(day, month)

    service = EventService(settings.API_BASE_ADDRESS)
    results = service.playlist(month, day)
    tracks = results['response']['tracks']

    track_ids = _get_track_ids(tracks)
    request.session['tracks'] = track_ids

    playlist = _get_spotify_embed_playlist(request, track_ids, date)

    return render(request, 'playlist.html', {
        'date': date,
        'tracks': tracks,
        'track_ids': track_ids,
        'playlist': playlist
    })


def add_to_spotify(request):
    auth_url = SPOTIFY_OAUTH.get_authorize_url()
    return redirect(auth_url)


def add_to_spotify_callback(request):
    today = datetime.now().strftime(PLAYLIST_DATE_FORMAT)
    code = request.GET.get('code', None)

    if code:
        tracks = request.session.get('tracks', None)

        service = SpotifyService(SPOTIFY_OAUTH, request.session)
        service.create_token(code)

        username = service.me()
        request.session['username'] = username

        _create_playlist(request, service, today, tracks, username)

        return redirect('playlist')

    return HttpResponseBadRequest()


def _get_date_from_month_day_values(day=None, month=None):
    today = datetime.now()

    if day is None and month is None:
        return today

    return datetime.strptime(
        '{} {} {}'.format(day, month, today.year), '%d %B %Y')


def _get_spotify_embed_playlist(request, tracks, requested_date):
    playlist_id = request.session.get('spotify_playlist_id')
    username = request.session.get('username')

    if not all([playlist_id, username]):
        return None

    pretty_date = requested_date.strftime(PLAYLIST_DATE_FORMAT)
    playlist_date = request.session.get('date')

    service = SpotifyService(SPOTIFY_OAUTH, request.session)

    if pretty_date != playlist_date:
        playlist = _create_playlist(request, service, pretty_date, tracks, username)
    else:
        playlist = service.get_playlist(username, playlist_id)

    return playlist['url']


def _create_playlist(request, service, playlist_date, tracks, username):
    playlist_name = 'Playlist a day for %s' % playlist_date
    playlist = service.create_playlist_with_tracks(username, playlist_name, tracks)
    request.session['spotify_playlist_id'] = playlist['id']
    request.session['date'] = playlist_date

    return playlist


def _get_track_ids(tracks):
    return ",".join([_remove_spotify_prefix(track) for track in tracks])


def _remove_spotify_prefix(track):
    return track['spotifyId'].rsplit(':', 1)[1]


def about_page(request):
    return render(request, 'about.html')


def _get_current_page(request):
    return int(request.GET.get('page', 1))


def _page_range(total):
    return range(1, 1 + ceil(total / EventService.RESULTS_PER_PAGE))


def _transform_api_response_to_model_list(events):
    return [_api_event_to_event_model(event) for event in events]


def _api_event_to_event_model(event):
    name = event.get('name', None)

    return Event(event["date"], event["description"], event["type"], name)


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
