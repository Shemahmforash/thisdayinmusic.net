import time
from math import ceil

import spotipy
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from spotipy import oauth2

from events.services.EventService import EventService
from thisdayinmusic.settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI


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


def playlist_page(request):
    date = datetime.now()

    service = EventService(settings.API_BASE_ADDRESS)
    results = service.playlist()
    tracks = results['response']['tracks']

    track_ids = _get_track_ids(tracks)
    playlist = _get_spotify_embed_playlist(request, track_ids)

    return render(request, 'playlist.html', {
        'date': date,
        'tracks': tracks,
        'track_ids': track_ids,
        'playlist': playlist
    })


def add_to_spotify(request):
    date = datetime.now().strftime('%A, %d %B %Y')
    code = request.GET.get('code', None)

    username = request.session.get('username', None)
    if not username:
        username = request.POST.get('username', None)
        request.session['username'] = username

    tracks = request.session.get('tracks', None)
    if not tracks:
        tracks = request.POST.get('tracks')
        request.session['tracks'] = tracks

    scope = 'playlist-modify-public,playlist-modify-private'
    spotify_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=scope)

    if code:
        token_info = spotify_oauth.get_access_token(code)
        request.session['spotify_token'] = token_info

        spotify = spotipy.Spotify(auth=token_info['access_token'])

        playlist = _create_playlist(spotify, username, date, tracks)

        request.session['spotify_playlist_id'] = playlist['id']
        request.session['date'] = date
        return redirect('playlist')
    else:
        auth_url = spotify_oauth.get_authorize_url()
        return redirect(auth_url)


def _create_playlist(spotify, username, date, track_ids):
    playlist = spotify.user_playlist_create(username, 'Playlist a day for %s' % date)

    track_list = track_ids.split(',')
    spotify.user_playlist_add_tracks(username, playlist['id'], track_list)

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


def _validate_token(spotify_oauth, token):
    expires_at = token['expires_at']
    now = int(time.time())

    if now > expires_at:
        token = spotify_oauth.refresh_access_token(token['refresh_token'])

    return token


def _get_spotify_embed_playlist(request, tracks):
    playlist_id = request.session.get('spotify_playlist_id')
    token = request.session.get('spotify_token')
    username = request.session.get('username')

    if not all([playlist_id, token, username]):
        return None

    today = datetime.now().strftime('%A, %d %B %Y')
    playlist_date = request.session.get('date')

    scope = 'playlist-modify-public,playlist-modify-private'
    spotify_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=scope)

    token = _validate_token(spotify_oauth, token)
    request.session['spotify_token'] = token

    spotify = spotipy.Spotify(auth=token['access_token'])

    if today != playlist_date:
        del request.session['date']
        del request.session['spotify_playlist_id']

        playlist = _create_playlist(spotify, username, today, tracks)

        request.session['spotify_playlist_id'] = playlist['id']
        request.session['date'] = today
    else:
        playlist = spotify.user_playlist(username, playlist_id)

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
