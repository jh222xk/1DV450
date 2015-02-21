from django.core.urlresolvers import reverse

from selenium.webdriver.common.keys import Keys


class TestCaseUtils(object):
    def login(self):
        # Edith goes to the login page
        self.browser.get(self.server_url + reverse('login'))

        # She fills in the inputs
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('edith')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('password')
        password_field.send_keys(Keys.RETURN)