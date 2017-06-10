from django.test import LiveServerTestCase
from datetime import datetime
from selenium import webdriver


class MainPageTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_main_page(self):
        self.browser.get(self.live_server_url)

        self.assertIn('This Day in Music', self.browser.title)

        today = datetime.now()

        header = self.browser.find_element_by_xpath(
            '/html/body/h1'
        ).text
        self.assertIn(
            today.strftime('%d'), header
        )
        self.assertIn(
            today.strftime("%B"), header
        )

        header_description = self.browser.find_element_by_xpath(
            '/html/body/h2'
        ).text
        self.assertIn(
            'Events that happened on this day in music...', header_description
        )

    def test_main_page_presents_event_list(self):
        self.browser.get(self.live_server_url)

        event_list = self.browser.find_elements_by_tag_name('h3')
        self.assertGreater(len(event_list), 1)
