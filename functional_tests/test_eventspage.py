import requests_mock
from django.test import LiveServerTestCase
from datetime import datetime
from django.conf import settings
from selenium import webdriver
import random


class EventsPageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    @staticmethod
    def given_a_random_date():
        return datetime.strptime(
            '{} {}'.format(random.randint(1, 366), 2017), '%j %Y')

    @requests_mock.Mocker()
    def test_can_open_events_page(self, m):
        date = self.given_a_random_date()

        m.get(settings.API_BASE_ADDRESS + '/event/?offset=0&month=' + date.strftime('%m') + '&day=' + date.strftime('%d'),
              json={
                  "response": {
                      "status": {
                          "version": 0.1,
                          "code": 0,
                          "status": "Success"
                      },
                      "events": [
                      ],
                      "pagination": {
                          "total": 59,
                          "offset": 0,
                          "results": 15
                      }
                  }
              }, status_code=200)

        month = date.strftime('%B')
        day = date.strftime("%d")

        self.browser.get('%s%s%s/%s' % (
            self.live_server_url, '/events/', month, day))

        self.assertIn('This Day in Music', self.browser.title)

        header = self.browser.find_element_by_class_name(
            'page-header'
        ).find_element_by_tag_name('h1').text
        self.assertIn(
            day, header
        )
        self.assertIn(month, header)

        self.assertIn(
            'Events that happened on this day in music...', header
        )

        pagination = self.browser.find_element_by_class_name('pagination')
        self.assertIsNotNone(pagination)

    @requests_mock.Mocker()
    def test_events_page_presents_event_list(self, m):
        date = self.given_a_random_date()

        m.get(settings.API_BASE_ADDRESS + '/event/?offset=0&month=' + date.strftime('%m') + '&day=' + date.strftime('%d'),
              json={
                  "response": {
                      "status": {
                          "version": 0.1,
                          "code": 0,
                          "status": "Success"
                      },
                      "events": [
                          {
                              "date": "1909-06-27",
                              "description": "Gianandrea Gavazzeni, composer was born",
                              "type": "Birth"
                          },
                      ],
                      "pagination": {
                          "total": 59,
                          "offset": 0,
                          "results": 15
                      }
                  }
              }, status_code=200)

        month = date.strftime('%B')
        day = date.strftime("%d")

        self.browser.get('%s%s%s/%s' % (
            self.live_server_url, '/events/', month, day))

        event_list = self.browser.find_elements_by_class_name('well')
        self.assertEqual(len(event_list), 1)
