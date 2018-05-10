import time

import spotipy


class SpotifyService:
    def __init__(self, spotify_oauth):
        self.spotify_oauth = spotify_oauth

    def get_playlist(self, username, playlist_id, token):
        spotify = self._get_spotify_connector(token)
        playlist = spotify.user_playlist(username, playlist_id)

        transformed_playlist = transform_spotify_playlist_to_thisdayinmusic_playlist(playlist)

        return transformed_playlist

    def create_playlist_with_tracks(self, username, playlist_name, tracks, token):
        spotify = self._get_spotify_connector(token)

        playlist = spotify.user_playlist_create(username, playlist_name)
        track_list = tracks.split(',')

        spotify.user_playlist_add_tracks(username, playlist['id'], track_list)

        return transform_spotify_playlist_to_thisdayinmusic_playlist(playlist)

    def _get_spotify_connector(self, token):
        expires_at = token['expires_at']
        now = int(time.time())

        if now > expires_at:
            token = self.spotify_oauth.refresh_access_token(token['refresh_token'])

        return spotipy.Spotify(auth=token['access_token'])


def convert_playlist_url_to_embed(url):
    return url.replace('/user/', '/embed/user/')


def transform_spotify_playlist_to_thisdayinmusic_playlist(playlist):
    url_embed = convert_playlist_url_to_embed(playlist['external_urls']['spotify'])

    return {
        'id': playlist['id'],
        'url': url_embed
    }
