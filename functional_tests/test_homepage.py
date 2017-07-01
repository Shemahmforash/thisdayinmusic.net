import requests_mock
from django.conf import settings
from django.test import LiveServerTestCase
from datetime import datetime
from selenium import webdriver


class MainPageTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    @requests_mock.Mocker()
    def test_can_open_main_page(self, m):
        m.get(settings.API_BASE_ADDRESS + '/event/', json={
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

        self.browser.get(self.live_server_url)

        self.assertIn('This Day in Music', self.browser.title)

        today = datetime.now()

        header = self.browser.find_element_by_class_name(
            'page-header'
        ).find_element_by_tag_name('h1').text
        self.assertIn(
            today.strftime('%d'), header
        )
        self.assertIn(
            today.strftime("%B"), header
        )

        self.assertIn(
            'Events that happened on this day in music...', header
        )

    @requests_mock.Mocker()
    def test_main_page_presents_event_list(self, m):
        m.get(settings.API_BASE_ADDRESS + '/event/', json={
            "response": {
                "status": {
                    "version": 0.1,
                    "code": 0,
                    "status": "Success"
                },
                "events": [
                    {
                        "date": "1908-06-27",
                        "description": "Hans de Jong, musician/conductor (De Damrakkertjes) was born",
                        "type": "Birth"
                    },
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
        self.browser.get(self.live_server_url)

        event_list = self.browser.find_elements_by_class_name('well')
        self.assertEqual(len(event_list), 2)

