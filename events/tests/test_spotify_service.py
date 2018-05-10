import time

from spotipy import oauth2
from unittest import TestCase, mock

from events.services.SpotifyService import SpotifyService
from thisdayinmusic.settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SPOTIFY_SCOPE


class SpotifyServiceTest(TestCase):
    def setUp(self):
        spotify_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SPOTIFY_SCOPE)
        self.service = SpotifyService(spotify_oauth)

    @mock.patch('spotipy.Spotify.user_playlist', return_value={'id': 'random_id', 'external_urls': {
        'spotify': 'https://open.spotify.com/user/random_user_name/playlist/random_id'}})
    def test_get_playlist_with_valid_token(self, user_playlist_mock):
        username = 'random_user_name'
        playlist_id = 'random_id'
        token = {
            'access_token': 'random_access_token',
            'expires_at': int(time.time()) + 3600,
        }

        playlist = self.service.get_playlist(username, playlist_id, token)

        self.assertIn(
            mock.call(
                'random_user_name', 'random_id'
            ),
            user_playlist_mock.call_args_list
        )

        self.assertEqual(playlist, {
            'id': 'random_id',
            'url': 'https://open.spotify.com/embed/user/random_user_name/playlist/random_id'
        })

    @mock.patch('spotipy.Spotify.user_playlist', return_value={'id': 'random_id', 'external_urls': {
        'spotify': 'https://open.spotify.com/user/random_user_name/playlist/random_id'}})
    @mock.patch('spotipy.oauth2.SpotifyOAuth.refresh_access_token', return_value={
        'access_token': 'new_access_token',
        'expires_at': 1000000
    })
    def test_get_playlist_with_expired_token_refreshes_it(self, refresh_access_token_mock, _):
        username = 'random_user_name'
        playlist_id = 'random_id'
        token = {
            'access_token': 'random_access_token',
            'expires_at': 10,
            'refresh_token': 'random_refresh_token'
        }

        playlist = self.service.get_playlist(username, playlist_id, token)

        self.assertIn(
            mock.call(
                'random_refresh_token'
            ),
            refresh_access_token_mock.call_args_list
        )

        self.assertEqual(playlist, {
            'id': 'random_id',
            'url': 'https://open.spotify.com/embed/user/random_user_name/playlist/random_id'
        })

    @mock.patch('spotipy.Spotify.user_playlist_create', return_value={'id': 'random_id', 'external_urls': {
        'spotify': 'https://open.spotify.com/user/random_user_name/playlist/random_id'}})
    @mock.patch('spotipy.Spotify.user_playlist_add_tracks')
    def test_create_playlist_with_valid_token(self, user_playlist_add_tracks_mock, user_playlist_create_mock):
        username = 'random_user_name'
        playlist_name = 'random_id'
        token = {
            'access_token': 'random_access_token',
            'expires_at': int(time.time()) + 3600,
        }
        tracks = 'random_id1,random_id2'

        playlist = self.service.create_playlist_with_tracks(username, playlist_name, tracks, token)
        self.assertIn(
            mock.call(
                username, playlist_name
            ),
            user_playlist_create_mock.call_args_list
        )

        self.assertIn(
            mock.call(
                username, 'random_id', ['random_id1', 'random_id2']
            ),
            user_playlist_add_tracks_mock.call_args_list
        )

        self.assertEqual(playlist, {
            'id': 'random_id',
            'url': 'https://open.spotify.com/embed/user/random_user_name/playlist/random_id'
        })
