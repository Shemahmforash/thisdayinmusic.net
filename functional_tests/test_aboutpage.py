from django.test import LiveServerTestCase
from selenium import webdriver

from functional_tests.utils import navbar_active_element_text


class AboutPageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_about_page(self):
        self.browser.get(self.live_server_url + '/about')

        self.assertIn('This Day in Music', self.browser.title)

        header = self.browser.find_element_by_class_name(
            'jumbotron'
        ).find_element_by_tag_name('h1').text

        self.assertIn(
            'This Day in Music', header
        )

        active_element = navbar_active_element_text(self.browser)
        self.assertIn("About", active_element)
