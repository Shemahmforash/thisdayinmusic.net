from django.test import LiveServerTestCase
from datetime import datetime
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

    def test_can_open_events_page(self):
        date = self.given_a_random_date()
        month = date.strftime('%B')
        day = date.strftime("%d")

        self.browser.get('%s%s%s/%s' % (
            self.live_server_url, '/events/', month, day))

        self.assertIn('This Day in Music', self.browser.title)

        header = self.browser.find_element_by_xpath(
            '/html/body/h1'
        ).text
        self.assertIn(
            day, header
        )
        self.assertIn(month, header)

        header_description = self.browser.find_element_by_xpath(
            '/html/body/h2'
        ).text
        self.assertIn(
            'Events that happened on this day in music...', header_description
        )
