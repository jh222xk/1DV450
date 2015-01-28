from django.core.urlresolvers import reverse

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the login page
        self.browser.get(self.server_url + reverse('login'))

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_username')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            480,
            delta=5
        )
