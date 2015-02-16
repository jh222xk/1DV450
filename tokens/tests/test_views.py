import base64
from json import loads
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token


class TokenTest(TestCase):

    """
    Test for tokens
    """

    def test_to_view_token_requires_login(self):
        """
        Test method for checking that to view token
        requires user to be logged in
        """
        # Send request to the positions API
        response = self.client.get(reverse('tokens:list'))

        # Check that we cannot access that url (redirection to the login url)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse(
            'tokens:list')), status_code=302, target_status_code=200)

    def test_to_create_a_new_token_requires_login(self):
        """
        Test method for checking that to view token
        requires user to be logged in
        """
        # Send request to the positions API
        response = self.client.get(reverse('tokens:new'))

        # Check that we cannot access that url (redirection to the login url)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse(
            'tokens:new')), status_code=302, target_status_code=200)


    def test_to_create_a_new_token_requires_login(self):
        """
        Test method for checking that to create a new token
        requires user to be logged in
        """
        # Send request to the positions API
        response = self.client.get(reverse('tokens:new'))

        # Check that we cannot access that url (redirection to the login url)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse(
            'tokens:new')), status_code=302, target_status_code=200)


    def test_to_delete_a_token_requires_login(self):
        """
        Test method for checking that delete a view token
        requires user to be logged in
        """
        # Send request to the positions API
        response = self.client.get(reverse('tokens:delete', kwargs={'pk': 1}))

        # Check that we cannot access that url (redirection to the login url)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse(
            'tokens:delete', kwargs={'pk': 1})), status_code=302, target_status_code=200)
