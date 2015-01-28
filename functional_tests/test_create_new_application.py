from django.core.urlresolvers import reverse

from .base import FunctionalTest


class CreateNewApplicationTest(FunctionalTest):

    def test_can_create_new_application(self):
        self.login()
        body = self.browser.find_element_by_tag_name('body')

        # After successfully logged in she goes to the creation of applications
        self.browser.get(self.server_url + reverse('oauth2_provider:register'))
        body = self.browser.find_element_by_tag_name('body')

        # She sees the new inputs
        self.assertIn('Register a new application', body.text)
        self.assertIn('Save', body.text)

        # She fills in the name
        name_field = self.browser.find_element_by_name('name')
        name_field.send_keys('Ediths APP')

        # And selects the client type
        client_type_field = self.browser.find_element_by_xpath(
            '//select[@name="client_type"]/option[text()="Public"]').click()

        # And select a authorization grant type
        authorization_grant_type_field = self.browser.find_element_by_xpath(
            '//select[@name="authorization_grant_type"]/option[text()="Resource owner password-based"]').click()

        # And fills in her redirect uri
        redirect_uris_field = self.browser.find_element_by_name(
            'redirect_uris')
        redirect_uris_field.send_keys('http://edith-amazing-app.com')

        # Then save it!
        button = self.browser.find_elements_by_xpath(
            "//*[@type='submit']")[0].click()

        # Redirection happens after creation so grab the new body
        body = self.browser.find_element_by_tag_name('body')

        # Check that our newly created app exists
        self.assertIn('Ediths APP', body.text)
        self.assertIn('Client secret', body.text)
        self.assertIn('Client id', body.text)
        self.assertIn('Edit', body.text)
        self.assertIn('Delete', body.text)
