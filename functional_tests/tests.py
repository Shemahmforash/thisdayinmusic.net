from django.test import LiveServerTestCase
from selenium import webdriver


class MainPageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_main_page(self):
        self.browser.get(self.live_server_url)

        self.assertIn('This Day in Music', self.browser.title)

        #  brand_text = self.browser.find_element_by_class_name(
        #  'navbar-brand'
        #  ).text
        #  self.assertIn('This Day In Music', brand_text)

        header_description = self.browser.find_element_by_xpath(
            '/html/body/h1/small'
        ).text
        self.assertIn(
            'Events that happened on this day in music...', header_description
        )

        event_list = self.browser.find_elements_by_tag_name('li')
        self.assertGreater(len(event_list), 1)
