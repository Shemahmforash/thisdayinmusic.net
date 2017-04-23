from django.test import TestCase
from unittest import mock
from events.services.EventService import EventService


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    @mock.patch('events.services.EventService.EventService.events')
    def test_call_event_service(self, mock_event_service_get):
        self.client.get('/')

        self.assertTrue(mock_event_service_get.called)


class EventServiceTest(TestCase):
    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_no_args_assumes_today(self, requests_mock):
        # given I call events with no args
        EventService.events()

        # then the api is reached without query parameters
        self.assertIn(
            mock.call(
                'http://thisdayinmusic.icdif.com/api/v0.1/event',
                params=None
            ),
            requests_mock.call_args_list
        )
