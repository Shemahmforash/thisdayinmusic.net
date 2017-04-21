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

        brand_text = self.browser.find_element_by_class_name(
                'navbar-brand'
                ).text
        self.assertIn('This Day In Music', brand_text)

        header = self.browser.find_element_by_tag_name('h1')
        header_description = header.find_element_by_tag_name('small')
        self.assertIn(
            'Events that happened on this day in music...', header_description
        )


if __name__ == '__main__':
    unittest.main()
