import time

import requests_mock
from datetime import datetime
from django.conf import settings
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from unittest import mock

from functional_tests.utils import navbar_active_element_text


class PlaylistPageTests(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    @requests_mock.Mocker()
    def test_can_open_playlist_page(self, m):
        m.get(settings.API_BASE_ADDRESS + '/playlist/', json={
            "response": {
                "status": {
                    "version": 0.1,
                    "code": 0,
                    "status": "Success"
                },
                "tracks": [
                ],
                "pagination": {
                    "total": 2,
                    "offset": 0,
                    "results": 2
                }
            }
        }, status_code=200)

        self.browser.get(self.live_server_url + '/playlist')

        today = datetime.now()

        date_text = '%s, %s' % (today.strftime('%B'), today.strftime('%d'))
        self.assertIn('Playlist a day for %s' % date_text, self.browser.title)

        header = self.browser.find_element_by_class_name(
            'page-header'
        ).find_element_by_tag_name('h1').text

        self.assertIn(
            'Playlist based on the events that happened on this day in music...',
            header
        )

        active_element = navbar_active_element_text(self.browser)
        self.assertIn("Playlist", active_element)

        self.assertRaises(NoSuchElementException, self.browser.find_element_by_id, 'date_picker')

    @requests_mock.Mocker()
    def test_playlist_page_shows_list_of_songs(self, m):
        m.get(settings.API_BASE_ADDRESS + '/playlist/', json={
            "response": {
                "status": {
                    "version": 0.1,
                    "code": 0,
                    "status": "Success"
                },
                "tracks": [
                    {
                        "name": "Zij Gelooft In Mij (2006 Digital Remaster)",
                        "artist": "Andre Hazes",
                        "spotifyId": "spotify-WW:track:4ZHCNqDss0HQchbrhleipg",
                        "event": "1951-06-30 - [Birth] Andre Hazes, Dutch barkeeper/singer (We Love Orange) was born"
                    },
                    {
                        "name": "He's Got the Whole World",
                        "artist": "Andrew Scott",
                        "spotifyId": "spotify-WW:track:3ZQsFBQVbWD7nDKkoSKB3q",
                        "event": "1949-06-30 - [Birth] Andrew Scott, Wales, rock guitarist (Sweet) was born"
                    }
                ],
                "pagination": {
                    "total": 2,
                    "offset": 0,
                    "results": 2
                }
            }
        }, status_code=200)

        self.browser.get(self.live_server_url + '/playlist')

        track_container = self.browser.find_element_by_class_name('well')
        self.assertIsNotNone(track_container)

        tracks = track_container.find_elements_by_tag_name('li')
        self.assertEqual(len(tracks), 2)

        self.assertEqual(tracks[0].text,
                         "1951-06-30 - [Birth] Andre Hazes, Dutch barkeeper/singer (We Love Orange) was born")
        self.assertEqual(tracks[1].text, "1949-06-30 - [Birth] Andrew Scott, Wales, rock guitarist (Sweet) was born")

    @requests_mock.Mocker()
    def test_playlist_page_shows_create_spotify_playlist_form(self, m):
        m.get(settings.API_BASE_ADDRESS + '/playlist/', json={
            "response": {
                "status": {
                    "version": 0.1,
                    "code": 0,
                    "status": "Success"
                },
                "tracks": [
                    {
                        "name": "Zij Gelooft In Mij (2006 Digital Remaster)",
                        "artist": "Andre Hazes",
                        "spotifyId": "spotify-WW:track:4ZHCNqDss0HQchbrhleipg",
                        "event": "1951-06-30 - [Birth] Andre Hazes, Dutch barkeeper/singer (We Love Orange) was born"
                    },
                    {
                        "name": "He's Got the Whole World",
                        "artist": "Andrew Scott",
                        "spotifyId": "spotify-WW:track:3ZQsFBQVbWD7nDKkoSKB3q",
                        "event": "1949-06-30 - [Birth] Andrew Scott, Wales, rock guitarist (Sweet) was born"
                    }
                ],
                "pagination": {
                    "total": 2,
                    "offset": 0,
                    "results": 2
                }
            }
        }, status_code=200)

        self.browser.get(self.live_server_url + '/playlist')

        create_spotify_playlist_form = self.browser.find_element_by_id('create-playlist')
        self.assertIsNotNone(create_spotify_playlist_form)

    @requests_mock.Mocker()
    @mock.patch('spotipy.Spotify.user_playlist', return_value={
        'id': '5jUBZBiQWmAiJaeJLYldcj',
        'external_urls': {
            'spotify': 'https://open.spotify.com/user/thesearchingwanderer/playlist/5jUBZBiQWmAiJaeJLYldcj?si=GgOazCjdR0uyHw6Vx9kCfQ'
        }})
    def test_playlist_page_shows_spotify_playlist(self, m, _):
        m.get(settings.API_BASE_ADDRESS + '/playlist/', json={
            "response": {
                "status": {
                    "version": 0.1,
                    "code": 0,
                    "status": "Success"
                },
                "tracks": [
                    {
                        "name": "Zij Gelooft In Mij (2006 Digital Remaster)",
                        "artist": "Andre Hazes",
                        "spotifyId": "spotify-WW:track:4ZHCNqDss0HQchbrhleipg",
                        "event": "1951-06-30 - [Birth] Andre Hazes, Dutch barkeeper/singer (We Love Orange) was born"
                    },
                    {
                        "name": "He's Got the Whole World",
                        "artist": "Andrew Scott",
                        "spotifyId": "spotify-WW:track:3ZQsFBQVbWD7nDKkoSKB3q",
                        "event": "1949-06-30 - [Birth] Andrew Scott, Wales, rock guitarist (Sweet) was born"
                    }
                ],
                "pagination": {
                    "total": 2,
                    "offset": 0,
                    "results": 2
                }
            }
        }, status_code=200)

        session = self.client.session
        session.save()
        self.browser.get(self.live_server_url)

        self.browser.add_cookie({'name': settings.SESSION_COOKIE_NAME, 'value': session.session_key})
        session['spotify_playlist_id'] = '5jUBZBiQWmAiJaeJLYldcj'
        session['username'] = 'thesearchingwanderer'
        session['date'] = datetime.now().strftime('%A, %d %B %Y')
        session['spotify_token'] = {
            'access_token': 'random',
            'expires_at': int(time.time()) + 3600
        }
        session.save()

        self.browser.get(self.live_server_url + '/playlist')

        spotify_playlist = self.browser.find_element_by_id('spotify-playlist')
        self.assertIsNotNone(spotify_playlist)
