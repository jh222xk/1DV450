from django.core.urlresolvers import reverse

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith goes to the login page
        self.browser.get(self.server_url + reverse('login'))

        # She notices the input box is nicely centered
        input_box = self.browser.find_element_by_id('id_username')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            200,
            delta=5
        )
