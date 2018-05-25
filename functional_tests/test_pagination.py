import requests_mock
from django.conf import settings

from functional_tests.selenium_test_case import SeleniumTestCase


class PaginationTest(SeleniumTestCase):
    @requests_mock.Mocker()
    def test_main_page_presents_pagination(self, m):
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

        pagination = self.browser.find_element_by_class_name('pagination')
        self.assertIsNotNone(pagination)

        active_page = pagination.find_element_by_class_name('active').text

        self.assertIn('1\n(current)', active_page)

    @requests_mock.Mocker()
    def test_events_page_presents_pagination(self, m):
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
        self.browser.get('%s/events/May/02' %
                         self.live_server_url)
        pagination = self.browser.find_element_by_class_name('pagination')
        self.assertIsNotNone(pagination)

        active_page = pagination.find_element_by_class_name('active').text

        self.assertIn('1\n(current)', active_page)

    @requests_mock.Mocker()
    def test_main_page_has_correct_page_selected(self, m):
        m.get(settings.API_BASE_ADDRESS + '/event/?offset=15', json={
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
                    "offset": 15,
                    "results": 15
                }
            }
        }, status_code=200)
        self.browser.get(self.live_server_url + '?page=2')

        pagination = self.browser.find_element_by_class_name('pagination')
        self.assertIsNotNone(pagination)

        active_page = pagination.find_element_by_class_name('active').text

        self.assertIn('2\n(current)', active_page)

    @requests_mock.Mocker()
    def test_events_page_has_correct_page_selected(self, m):
        m.get(settings.API_BASE_ADDRESS + '/event/?offset=30', json={
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
                    "offset": 30,
                    "results": 15
                }
            }
        }, status_code=200)

        self.browser.get('%s/events/May/02?page=3' %
                         self.live_server_url)

        pagination = self.browser.find_element_by_class_name('pagination')
        self.assertIsNotNone(pagination)

        active_page = pagination.find_element_by_class_name('active').text

        self.assertIn('3\n(current)', active_page)
