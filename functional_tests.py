from selenium import webdriver
import unittest


class MainPageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_open_main_page(self):
        self.browser.get('http://127.0.0.1:8000')

        self.assertIn('This Day in Music', self.browser.title)


if __name__ == '__main__':
    unittest.main()
