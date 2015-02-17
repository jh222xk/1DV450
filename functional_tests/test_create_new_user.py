from django.core.urlresolvers import reverse

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class CreateNewUserTest(FunctionalTest):

    def test_user_can_create_new_user(self):
        """
        Test for checking if user can be created
        with valid credentials
        """

        # Edith goes to the register page
        self.browser.get(self.server_url + reverse('register'))

        # She fills in the inputs
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('netuser')
        password_field = self.browser.find_element_by_name('password1')
        password_field.send_keys('password')
        password_confirmation_field = self.browser.find_element_by_name('password2')
        password_confirmation_field.send_keys('password')
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('netuser@edith.com')

        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        # Edith sees a congratulations message
        self.assertIn('Congratulations! You are now registered and logged in!', body.text)

        # After successfully logged in she goes to her applications
        # self.browser.get(self.server_url + reverse('tokens:list'))

        # body = self.browser.find_element_by_tag_name('body')
        # self.assertIn('Your token', body.text)

    def test_raise_error_if_username_already_exists(self):
        """
        Test for checking if errors appear if username
        already exists
        """
        # Edith goes to the register page
        self.browser.get(self.server_url + reverse('register'))

        # She fills in the inputs

        # Username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('edith')

        # Password
        password_field = self.browser.find_element_by_name('password1')
        password_field.send_keys('password')

        # Password confirm
        password_confirmation_field = self.browser.find_element_by_name('password2')
        password_confirmation_field.send_keys('password')

        # Email
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('netuser@edith.com')

        # Submit the form!
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        # Edith sees error message
        self.assertIn('A user with that username already exists.', body.text)


    def test_raise_error_if_email_already_exists(self):
        """
        Test for checking if errors appear if email
        already exists
        """
        # Edith goes to the register page
        self.browser.get(self.server_url + reverse('register'))

        # She fills in the inputs

        # Username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('netuser')

        # Password
        password_field = self.browser.find_element_by_name('password1')
        password_field.send_keys('password')

        # Password confirm
        password_confirmation_field = self.browser.find_element_by_name('password2')
        password_confirmation_field.send_keys('password')

        # Email
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('edith@edith.com')

        # Submit the form!
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        # Edith sees error message
        self.assertIn('This email address already exists.', body.text)

    def test_raise_error_if_password_does_not_match(self):
        """
        Test for checking if errors appear if the passwords
        does not match
        """
        # Edith goes to the register page
        self.browser.get(self.server_url + reverse('register'))

        # She fills in the inputs
        # Username
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('netuser')

        # Password
        password_field = self.browser.find_element_by_name('password1')
        password_field.send_keys('password')

        # Password confirm
        password_confirmation_field = self.browser.find_element_by_name('password2')
        password_confirmation_field.send_keys('not_the_same_password')

        # Email
        email_field = self.browser.find_element_by_name('email')
        email_field.send_keys('edith@edith.com')

        # Submit the form!
        password_field.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')

        # Edith sees error message
        self.assertIn('The two password fields didn\'t match.', body.text)
