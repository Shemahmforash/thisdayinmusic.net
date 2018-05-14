import time

import spotipy


class TokenNotFoundException(Exception):
    pass


class SpotifyService:
    TOKEN_KEY = 'spotify_token'

    def __init__(self, spotify_oauth, backend=None):
        self.spotify_oauth = spotify_oauth
        self.backend = backend

    def me(self):
        spotify = self._get_spotify_connector()

        me = spotify.me()

        return transform_spotify_user_to_thisdayinmusic_user(me)

    def get_playlist(self, username, playlist_id):
        spotify = self._get_spotify_connector()
        playlist = spotify.user_playlist(username, playlist_id)

        transformed_playlist = transform_spotify_playlist_to_thisdayinmusic_playlist(playlist)

        return transformed_playlist

    def create_playlist_with_tracks(self, username, playlist_name, tracks):
        spotify = self._get_spotify_connector()

        playlist = spotify.user_playlist_create(username, playlist_name)
        track_list = tracks.split(',')

        spotify.user_playlist_add_tracks(username, playlist['id'], track_list)

        return transform_spotify_playlist_to_thisdayinmusic_playlist(playlist)

    def create_token(self, code):
        token = self.spotify_oauth.get_access_token(code)
        self.backend[self.TOKEN_KEY] = token

    def _get_spotify_connector(self):
        token = self.backend.get(self.TOKEN_KEY, None)
        if not token:
            raise TokenNotFoundException

        expires_at = token['expires_at']
        now = int(time.time())

        if now > expires_at:
            token = self.spotify_oauth.refresh_access_token(token['refresh_token'])
            self.backend[self.TOKEN_KEY] = token

        return spotipy.Spotify(auth=token['access_token'])


def convert_playlist_url_to_embed(url):
    return url.replace('/user/', '/embed/user/')


def transform_spotify_playlist_to_thisdayinmusic_playlist(playlist):
    url_embed = convert_playlist_url_to_embed(playlist['external_urls']['spotify'])

    return {
        'id': playlist['id'],
        'url': url_embed
    }


def transform_spotify_user_to_thisdayinmusic_user(user):
    return user['id']
