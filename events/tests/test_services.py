from unittest import mock

from django.test import TestCase

from events.services.EventService import EventService
from events.tests.utils import given_a_random_page


class EventServiceTest(TestCase):

    def test_that_offset_for_page_1_is_zero(self):
        page = 1

        self.assertEqual(0, EventService.offset(page))

    def test_that_offset_for_page_0_is_zero(self):
        page = 0

        self.assertEqual(0, EventService.offset(page))

    def test_that_offset_for_negative_page_is_zero(self):
        page = given_a_random_page() * (-1)

        self.assertEqual(0, EventService.offset(page))

    def test_that_offset_is_equal_to_the_number_of_results_per_page_for_page_2(self):
        page = 2

        self.assertEqual(EventService.RESULTS_PER_PAGE, EventService.offset(page))

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_no_args_api_is_called_with_no_args(
            self, requests_mock):
        # given I call events with no args
        EventService.events()

        # then the api is reached without query parameters
        self.assertIn(
            mock.call(
                EventService.API_ADDRESS,
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
                EventService.API_ADDRESS,
                params=None
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_month_args_api_is_called_with_no_args(
            self, requests_mock):
        # given I call events with month
        EventService.events(month='April')

        # then the api is reached without query parameters
        self.assertIn(
            mock.call(
                EventService.API_ADDRESS,
                params=None
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_day_and_month_args_api_is_called_with_day_and_month(
            self, requests_mock):
        # given I call events with day and month
        EventService.events(month='April', day=1)

        # then the api is reached with day and month as query parameters
        self.assertIn(
            mock.call(
                EventService.API_ADDRESS,
                params={'day': '01', 'month': '04', 'offset': 0}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.get')
    def test_events_with_day_month_args_api_is_called_with_day_and_month(
            self, requests_mock):
        page = given_a_random_page()

        offset = EventService.offset(page)

        # given I call events with day and month
        EventService.events(month='April', day=1, page=page)

        # then the api is reached with day and month as query parameters
        self.assertIn(
            mock.call(
                EventService.API_ADDRESS,
                params={'day': '01', 'month': '04', 'offset': offset}
            ),
            requests_mock.call_args_list
        )

    @mock.patch('events.services.EventService.requests.models.Response.json',
                return_value={"response": {"events": [{}]}})
    def test_when_api_returns_results_events_should_return_them(
            self, mocked):
        # given that the api responds with a json
        result = EventService.events()

        # then a dictionary is returned
        self.assertEqual(type(result), dict)

        # with the right keys
        self.assertEqual(result['response'], {"events": [{}]})
