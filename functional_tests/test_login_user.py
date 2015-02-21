from django.core.urlresolvers import reverse

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LoginUserTest(FunctionalTest):

    def test_user_can_login_with_valid_credentials(self):
        """
        Test for checking if user can login with
        valid credentials
        """

        # Edith goes to the login page
        self.browser.get(self.server_url + reverse('login'))

        # She fills in the inputs
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('edith')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password')
        password_field.send_keys(Keys.RETURN)

        # After successfully logged in she goes to her applications
        self.browser.get(self.server_url + reverse('tokens:list'))

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Your token', body.text)

    def test_user_cannot_login_with_INVALID_credentials(self):
        """
        Test for checking if user cannot login with
        INVALID credentials
        """

        # Edith goes to the login page
        self.browser.get(self.server_url + reverse('login'))

        # She fills in her beautiful name
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('edith')

        # She cant really remember her password...
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('whatsmypassword')

        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        # She sees an error message.
        self.assertIn('Please enter a correct username and password. Note that both fields may be case-sensitive.', body.text)
