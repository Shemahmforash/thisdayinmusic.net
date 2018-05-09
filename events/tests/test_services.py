from django.conf import settings
from django.test import TestCase
from unittest import mock
from unittest.mock import ANY

from events.services.EventService import EventService
from events.tests.utils import given_a_random_page


class EventServiceTest(TestCase):
    def setUp(self):
        self.service = EventService(settings.API_BASE_ADDRESS)

    def test_that_offset_for_page_1_is_zero(self):
        page = 1

        self.assertEqual(0, self.service.offset(page))

    def test_that_offset_for_page_0_is_zero(self):
        page = 0

        self.assertEqual(0, self.service.offset(page))

    def test_that_offset_for_negative_page_is_zero(self):
        page = given_a_random_page() * (-1)

        self.assertEqual(0, self.service.offset(page))

    def test_that_offset_is_equal_to_the_number_of_results_per_page_for_page_2(self):
        page = 2

        self.assertEqual(15, self.service.offset(page))

    def test_that_offset_is_equal_to_twice_the_number_of_results_per_page_for_page_3(self):
        page = 3

        self.assertEqual(30, self.service.offset(page))

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_no_args_api_is_called_with_default_args(
            self, requests_mock):
        # given I call events with no args
        self.service.events()

        # then the api is reached with default query parameters
        self.assertIn(
            mock.call(
                ANY,
                params={'offset': 0, 'fields[]': ['artist', 'date', 'description', 'type']}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_day_args_api_is_called_with_default_args(
            self, requests_mock):
        # given I call events with day
        self.service.events(day=10)

        # then the api is reached with default query parameters
        self.assertIn(
            mock.call(
                ANY,
                params={'offset': 0, 'fields[]': ['artist', 'date', 'description', 'type']}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_month_args_api_is_called_with_default_args(
            self, requests_mock):
        # given I call events with month
        self.service.events(month='April')

        # then the api is reached with default query parameters
        self.assertIn(
            mock.call(
                ANY,
                params={'offset': 0, 'fields[]': ['artist', 'date', 'description', 'type']}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_page_args_api_is_called_with_the_right_offset_args(
            self, requests_mock):
        page = 2

        # given I call events with no args
        self.service.events(page=page)

        # then the api is reached without query parameters
        self.assertIn(
            mock.call(
                ANY,
                params={'offset': 15, 'fields[]': ['artist', 'date', 'description', 'type']}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_day_and_month_args_api_is_called_with_day_and_month(
            self, requests_mock):
        # given I call events with day and month
        self.service.events(month='April', day=1)

        # then the api is reached with day and month as query parameters
        self.assertIn(
            mock.call(
                ANY,
                params={'day': '01', 'month': '04', 'offset': 0, 'fields[]': ['artist', 'date', 'description', 'type']}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_day_month_and_page_args_api_is_called_with_day_and_month_and_offset(
            self, requests_mock):
        page = given_a_random_page()

        offset = self.service.offset(page)

        # given I call events with day and month
        self.service.events(month='April', day=1, page=page)

        # then the api is reached with day and month as query parameters
        self.assertIn(
            mock.call(
                ANY,
                params={'day': '01', 'month': '04', 'offset': offset,
                        'fields[]': ['artist', 'date', 'description', 'type']}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_when_api_returns_results_events_should_return_them(
            self, mocked_get):
        # given that the api responds with a json
        mocked_response = mock.MagicMock()
        mocked_response.json.return_value = {"response": {"events": [{}]}}
        mocked_get.return_value = mocked_response

        result = self.service.events()

        # then a dictionary is returned
        self.assertEqual(type(result), dict)

        # with the right keys
        self.assertEqual(result['response'], {"events": [{}]})

    @mock.patch('events.services.EventService.requests.get')
    def test_playlist_calls_the_right_api(self, requests_mock):
        # given I call events with no args
        self.service.playlist()

        # then the api is reached without query parameters
        self.assertIn(
            mock.call(
                ANY,
            ),
            requests_mock.call_args_list)
