from django.test import TestCase
from unittest import mock
from events.services.EventService import EventService


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


class EventServiceTest(TestCase):

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_no_args_api_is_called_with_no_args(
            self, requests_mock):
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

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_day_args_api_is_called_with_no_args(
            self, requests_mock):
        # given I call events with day
        EventService.events(day=10)

        # then the api is reached without query parameters
        self.assertIn(
            mock.call(
                'http://thisdayinmusic.icdif.com/api/v0.1/event',
                params=None
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_month_args_api_is_called_with_no_args(
            self, requests_mock):
        # given I call events with month
        EventService.events(month=10)

        # then the api is reached without query parameters
        self.assertIn(
            mock.call(
                'http://thisdayinmusic.icdif.com/api/v0.1/event',
                params=None
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_day_and_month_args_api_is_called_with_day_and_month(
            self, requests_mock):
        # given I call events with day and month
        EventService.events(month=10, day=20)

        # then the api is reached with day and month as query parameters
        self.assertIn(
            mock.call(
                'http://thisdayinmusic.icdif.com/api/v0.1/event',
                params={'day': 20, 'month': 10}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.models.Response.json',
                return_value={"response": {"events": [{}]}})
    def test_when_api_returns_results_events_should_return_them(
            self, response_json):
        # given that the api responds with a json
        result = EventService.events()

        # then a dictionary is returned
        self.assertEqual(type(result), dict)

        # with the right keys
        self.assertEqual(result['response'], {"events": [{}]})
