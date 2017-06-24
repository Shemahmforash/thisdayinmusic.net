from unittest import mock

from django.test import TestCase


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    @mock.patch('events.services.EventService.EventService.events')
    def test_home_page_today_calls_event_service(self, mock_event_service_get):
        self.client.get('/')

        self.assertTrue(mock_event_service_get.called)

    @mock.patch('events.services.EventService.EventService.events')
    def test_events_page_calls_event_service(self, mock_event_service_get):
        # when I access a random events page day
        self.client.get('/events/April/25')

        # then the service is called with the right arguments
        self.assertIn(
            mock.call(
                'April',
                '25'
            ),
            mock_event_service_get.call_args_list
        )