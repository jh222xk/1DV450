from django.core.urlresolvers import reverse

from .base import FunctionalTest


class LoginViaOauthTest(FunctionalTest):

    def test_can_login_via_oauth(self):
        self.login()
        body = self.browser.find_element_by_tag_name('body')

        # After successfully logged in she goes to her applications
        self.browser.get(self.server_url + reverse('oauth2_provider:list'))

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Your applications', body.text)
        self.assertIn(
            'No applications defined. Click here if you want to register a new one', body.text)
