from math import ceil

from datetime import datetime
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect

from events.services.event_service import EventService
from events.services.spotify_service import SpotifyService
from events.transformers.event_transformer import transform_event_api_response_to_model_list, \
    transform_playlist_to_track_list, transform_tracks_to_track_ids_string
from events.transformers.spotify_transformer import transform_spotify_playlist_to_thisdayinmusic_playlist
from thisdayinmusic.settings import SPOTIFY_OAUTH

PLAYLIST_DATE_FORMAT = '%A, %d %B %Y'


def home_page(request):
    page = _get_current_page(request)

    service = EventService(settings.API_BASE_ADDRESS)
    events = service.events(page=page)
    date = datetime.now()

    pagination = events['response']['pagination']

    return render(request, 'home.html', {
        'events': transform_event_api_response_to_model_list(events['response']['events']),
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
        'events': transform_event_api_response_to_model_list(events['response']['events']),
        'date': date,
        'current_page': page,
        'pages': _page_range(pagination['total'])
    })


def playlist_page(request, month=None, day=None):
    date = _get_date_from_month_day_values(day, month)

    service = EventService(settings.API_BASE_ADDRESS)
    results = service.playlist(month, day)

    tracks = transform_playlist_to_track_list(results)

    track_ids = transform_tracks_to_track_ids_string(tracks)
    request.session['tracks'] = track_ids

    playlist = _get_or_create_spotify_playlist(request, track_ids, date)

    return render(request, 'playlist.html', {
        'date': date,
        'tracks': tracks,
        'playlist': playlist
    })


def add_to_spotify(request):
    auth_url = SPOTIFY_OAUTH.get_authorize_url()
    return redirect(auth_url)


def add_to_spotify_callback(request):
    code = request.GET.get('code', None)

    if code:
        service = SpotifyService(SPOTIFY_OAUTH, request.session)
        service.create_token(code)

        username = service.me()
        request.session['username'] = username

        return redirect('playlist')

    return HttpResponseBadRequest()


def _get_date_from_month_day_values(day=None, month=None):
    today = datetime.now()

    if day is None and month is None:
        return today

    return datetime.strptime(
        '{} {} {}'.format(day, month, today.year), '%d %B %Y')


def _get_or_create_spotify_playlist(request, tracks, requested_date):
    playlist_id = request.session.get('spotify_playlist_id', None)
    username = request.session.get('username')
    playlist_date = request.session.get('date', None)

    if not username:
        return None

    pretty_date = requested_date.strftime(PLAYLIST_DATE_FORMAT)
    service = SpotifyService(SPOTIFY_OAUTH, request.session)

    if playlist_id and pretty_date == playlist_date:
        playlist = transform_spotify_playlist_to_thisdayinmusic_playlist(
            service.get_playlist(username, playlist_id)
        )
    else:
        playlist = _create_playlist(request, service, pretty_date, tracks, username)

    return playlist['url']


def _create_playlist(request, service, playlist_date, tracks, username):
    playlist_name = 'Playlist a day for %s' % playlist_date
    playlist = service.create_playlist_with_tracks(username, playlist_name, tracks)

    simplified_playlist = transform_spotify_playlist_to_thisdayinmusic_playlist(playlist)
    request.session['spotify_playlist_id'] = simplified_playlist['id']
    request.session['date'] = playlist_date

    return simplified_playlist


def about_page(request):
    return render(request, 'about.html')


def _get_current_page(request):
    return int(request.GET.get('page', 1))


def _page_range(total):
    return range(1, 1 + ceil(total / EventService.RESULTS_PER_PAGE))
