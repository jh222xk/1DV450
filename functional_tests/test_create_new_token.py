from django.core.urlresolvers import reverse

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class CreateNewTokenTest(FunctionalTest):

    def test_can_create_new_token(self):
        # Edith logins
        self.login()

        body = self.browser.find_element_by_tag_name('body')

        # She sees the new inputs
        self.assertIn('Your token', body.text)
        self.assertIn('You dont have any tokens...', body.text)
        self.assertIn('New token', body.text)

        # She clicks the button
        new_token_button = self.browser.find_element_by_name('new_token')
        new_token_button.click()

        # Redirection happens after creation so grab the new body
        body = self.browser.find_element_by_tag_name('body')

        # Edith sees that her newly created token has been created
        self.assertIn('Your token has been created!', body.text)
        self.assertIn('Delete', body.text)