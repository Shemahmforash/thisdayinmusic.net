import webbrowser
from math import ceil

import os

import spotipy
from django.shortcuts import render, redirect
from spotipy import util, Spotify, oauth2

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

    today = datetime.now()

    date = datetime.strptime(
        '{} {} {}'.format(day, month, today.year), '%d %B %Y')

    pagination = events['response']['pagination']

    return render(request, 'home.html', {
        'events': _transform_api_response_to_model_list(events['response']['events']),
        'date': date,
        'current_page': page,
        'pages': _page_range(pagination['total'])
    })


def add_to_spotify(request):
    date = datetime.now().strftime('%A, %d %B %Y')
    code = request.GET.get('code', None)

    tracks = request.session.get('tracks', None)
    if not tracks:
        tracks = request.POST.get('tracks')
        request.session['tracks'] = tracks

    scope = 'playlist-modify-public,playlist-modify-private'

    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scope)
    if code:
        token_info = sp_oauth.get_access_token(code)

        sp = spotipy.Spotify(auth=token_info['access_token'])

        playlist = sp.user_playlist_create('thesearchingwanderer', 'Playlist a day for %s' % date)
        request.session['playlist'] = playlist

        track_list = tracks.split(',')
        sp.user_playlist_add_tracks('thesearchingwanderer', playlist['id'], track_list)

        return redirect('playlist')
    else:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)


def playlist_page(request):
    date = datetime.now()

    playlist = _get_spotify_embed_playlist(request)

    service = EventService(settings.API_BASE_ADDRESS)
    results = service.playlist()
    tracks = results['response']['tracks']

    track_ids = _get_track_ids(tracks)

    return render(request, 'playlist.html', {
        'date': date,
        'tracks': tracks,
        'track_ids': track_ids,
        'playlist': playlist
    })


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


def _get_spotify_embed_playlist(request):
    playlist = request.session.get('playlist', None)

    if playlist:
        url = playlist['external_urls']['spotify']
        return url.replace('/user/', '/embed/user/')

    return None


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
