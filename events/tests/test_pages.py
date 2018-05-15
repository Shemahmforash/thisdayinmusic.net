import time

from datetime import datetime, timedelta
from django.test import TestCase
from unittest import mock

from events.tests.utils import given_a_random_page


class PagesTest(TestCase):
    @mock.patch('events.services.event_service.EventService.events')
    def test_homepage_uses_home_template(self, _):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    @mock.patch('events.services.event_service.EventService.events')
    def test_eventspage_uses_home_template(self, _):
        response = self.client.get('/events/April/25')
        self.assertTemplateUsed(response, 'home.html')

    @mock.patch('events.services.event_service.EventService.playlist')
    def test_playlistpage_uses_playlist_template(self, _):
        response = self.client.get('/playlist')
        self.assertTemplateUsed(response, 'playlist.html')

    @mock.patch('events.services.event_service.EventService.playlist')
    def test_playlistpage_for_certain_day_uses_playlist_template(self, _):
        response = self.client.get('/playlist/May/12')
        self.assertTemplateUsed(response, 'playlist.html')

    def test_aboutpage_uses_about_template(self):
        response = self.client.get('/about')
        self.assertTemplateUsed(response, 'about.html')

    @mock.patch('events.services.event_service.EventService.events')
    def test_home_page_calls_event_service(self, mock_event_service_get):
        self.client.get('/')

        self.assertTrue(mock_event_service_get.called)

    @mock.patch('events.services.event_service.EventService.events')
    def test_events_page_with_pagination_calls_event_service(self, mock_event_service_get):
        page = given_a_random_page()

        # when I access a random events page day
        self.client.get('/events/April/25?page=%d' % page)

        # then the service is called with the right arguments
        self.assertIn(
            mock.call(
                'April',
                '25',
                page
            ),
            mock_event_service_get.call_args_list
        )

    @mock.patch('events.services.event_service.EventService.events')
    def test_home_page_with_pagination_calls_event_service(self, mock_event_service_get):
        page = given_a_random_page()

        # when I access a particular page
        self.client.get('/?page=%d' % page)

        # then the service is called with that page
        self.assertIn(
            mock.call(
                page=page,
            ),
            mock_event_service_get.call_args_list
        )

    @mock.patch('events.services.event_service.EventService.playlist')
    def test_playlist_page_with_date_calls_event_service(self, mock_event_service_get):
        self.client.get('/playlist/April/25')

        # then the service is called with the right arguments
        self.assertIn(
            mock.call(
                'April',
                '25',
            ),
            mock_event_service_get.call_args_list
        )

    @mock.patch('events.services.event_service.EventService.playlist')
    def test_playlist_page_calls_event_service(self, mock_event_service_get):
        self.client.get('/playlist')

        self.assertTrue(mock_event_service_get.called)

    @mock.patch('events.services.event_service.EventService.playlist')
    @mock.patch('events.services.spotify_service.SpotifyService.get_playlist',
                return_value={
                    'id': 'random',
                    'external_urls': {
                        'spotify': 'url'
                    }
                })
    def test_playlist_page_gets_already_generated_playlist(self, spotify_get_playlist_mock, _):
        session = self.client.session
        session['spotify_playlist_id'] = 'xpto'
        session['username'] = 'some_user'
        session['spotify_token'] = {
            'access_token': 'random_access_token',
            'expires_at': int(time.time()) + 3600,
        }
        session['date'] = datetime.now().strftime('%A, %d %B %Y')
        session.save()

        self.client.get('/playlist')

        self.assertTrue(spotify_get_playlist_mock.called)

    @mock.patch('events.services.event_service.EventService.playlist')
    @mock.patch('events.services.spotify_service.SpotifyService.create_playlist_with_tracks',
                return_value={
                    'id': 'random',
                    'external_urls': {
                        'spotify': 'url'
                    }
                })
    def test_playlist_page_creates_playlist_when_date_is_not_the_same_as_generated(self,
                                                                                   create_playlist_with_tracks_mock,
                                                                                   _):
        past_date = datetime.now() - timedelta(days=1)
        session = self.client.session
        session['spotify_playlist_id'] = 'xpto'
        session['username'] = 'some_user'
        session['date'] = past_date.strftime('%A, %d %B %Y')
        session['spotify_token'] = {
            'access_token': 'random_access_token',
            'expires_at': int(time.time()) + 3600,
        }
        session.save()

        self.client.get('/playlist')

        self.assertTrue(create_playlist_with_tracks_mock.called)

    @mock.patch('events.services.event_service.EventService.playlist')
    @mock.patch('events.services.spotify_service.SpotifyService.create_playlist_with_tracks',
                return_value={
                    'id': 'random',
                    'external_urls': {
                        'spotify': 'url'
                    }
                })
    def test_playlist_page_with_date_creates_playlist_when_date_is_not_the_same_as_generated(self,
                                                                                             create_playlist_with_tracks_mock,
                                                                                             _):
        date = datetime.now()
        session = self.client.session
        session['spotify_playlist_id'] = 'xpto'
        session['username'] = 'some_user'
        session['date'] = date.strftime('%A, %d %B %Y')
        session['spotify_token'] = {
            'access_token': 'random_access_token',
            'expires_at': int(time.time()) + 3600,
        }
        session.save()

        # TODO: use dynamic date in url
        self.client.get('/playlist/May/11')

        self.assertTrue(create_playlist_with_tracks_mock.called)

    @mock.patch('spotipy.oauth2.SpotifyOAuth.get_authorize_url', return_value='/playlist')
    def test_add_to_spotify_page_redirects_to_spotify_auth(self, spotify_get_oauth_url_mock):
        response = self.client.post('/playlist/create_playlist', {'username': 'random', 'tracks': 'abc,def'})

        self.assertTrue(spotify_get_oauth_url_mock.called)
        self.assertRedirects(response, '/playlist')

    @mock.patch('events.services.spotify_service.SpotifyService.create_token')
    @mock.patch('events.services.spotify_service.SpotifyService.create_playlist_with_tracks',
                return_value={
                    'id': 'random',
                    'external_urls': {
                        'spotify': 'url'
                    }
                })
    @mock.patch('events.services.spotify_service.SpotifyService.me', return_value={'id': 'some_username'})
    def test_add_to_spotify_callback_page_creates_token_and_redirects_to_playlist(self,
                                                                                  spotify_me_mock,
                                                                                  create_playlist_with_tracks_mock,
                                                                                  spotify_create_token_mock):
        response = self.client.get('/playlist/create_playlist/callback?code=some_code')

        self.assertTrue(spotify_create_token_mock.called)
        self.assertTrue(spotify_me_mock.called)

        self.assertRedirects(response, '/playlist')

        self.assertTrue(create_playlist_with_tracks_mock.called)
