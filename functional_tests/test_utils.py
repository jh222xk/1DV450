from django.core.urlresolvers import reverse

from selenium.webdriver.common.keys import Keys


class TestCaseUtils(object):
    def login(self):
        # Edith goes to the api-auth login page
        self.browser.get(self.server_url + reverse('login'))

        body = self.browser.find_element_by_tag_name('body')

        # She fills in the inputs
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)