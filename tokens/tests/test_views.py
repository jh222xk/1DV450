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

    def setUp(self):
        """
        Here we set up our test objects for the tests
        """
        self.user_obj = User.objects.create_user('test', "asd@asd.se", 'password')

        self.token = Token.objects.create(
            user=self.user_obj
        )

    def tearDown(self):
        self.user_obj.delete()
        self.token.delete()

    def test_authorized_user_can_view_token(self):
        # Login user
        self.client.login(username='test', password='password')

        # Send request to the tokens list url
        response = self.client.get(reverse('tokens:list'))

        # Check that our token is there.
        self.assertEqual(response.context['tokens'][0], self.token)

    def test_to_view_token_requires_login(self):
        """
        Test method for checking that to view token
        requires user to be logged in
        """
        # Send request to the tokens list url
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
        # Send request to the tokens new url
        response = self.client.get(reverse('tokens:new'))

        # Check that we cannot access that url (redirection to the login url)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse(
            'tokens:new')), status_code=302, target_status_code=200)

    def test_to_delete_a_token_requires_login(self):
        """
        Test method for checking that delete a view token
        requires user to be logged in
        """
        # Send request to the tokens delete url
        response = self.client.get(reverse('tokens:delete', kwargs={'pk': 1}))

        # Check that we cannot access that url (redirection to the login url)
        self.assertRedirects(response, "%s?next=%s" % (reverse('login'), reverse(
            'tokens:delete', kwargs={'pk': 1})), status_code=302, target_status_code=200)

    def test_can_only_create_one_new_token(self):
        """
        Test method for checking that we only
        can create one token
        """

        # Login user
        self.client.login(username='test', password='password')

        # Grab our count
        count = Token.objects.filter(user=self.user_obj).count()

        # Make sure our count is one
        self.assertEqual(count, 1)

        # Try to create a new token
        response = self.client.post(reverse('tokens:new'))

        # Check that we redirects back to the list
        self.assertRedirects(response, reverse('tokens:list'), status_code=302, target_status_code=200)

        # Grab our count again
        count = Token.objects.filter(user=self.user_obj).count()

        # Make sure our count is the same
        self.assertEqual(count, 1)
