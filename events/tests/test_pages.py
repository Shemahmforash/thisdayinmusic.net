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
    def test_playlist_page_calls_event_service(self, mock_event_service_get):
        self.client.get('/playlist')

        self.assertTrue(mock_event_service_get.called)
