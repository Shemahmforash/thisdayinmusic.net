from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from events.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_homepage_returns_html(self):
        request = HttpRequest()

        response = home_page(request)
        self.assertEqual(response.status_code, 200)
