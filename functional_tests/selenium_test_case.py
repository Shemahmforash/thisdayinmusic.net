import socket
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


class SeleniumTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = socket.gethostbyname(socket.gethostname())
        super(SeleniumTestCase, cls).setUpClass()

    def setUp(self):
        self.browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.FIREFOX
        )

    def tearDown(self):
        self.browser.quit()
