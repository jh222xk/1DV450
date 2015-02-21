import sys

from django.contrib.staticfiles.testing import LiveServerTestCase

from selenium import webdriver

from .test_utils import TestCaseUtils


class FunctionalTest(TestCaseUtils, LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    fixtures = ['admin.json']

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        # self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
