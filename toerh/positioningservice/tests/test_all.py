from json import loads
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from provider.oauth2.models import Client

from ..models import Position


class UserAPITestCase(APITestCase):

    """
    Base API test class so we can have logged in user
    """

    api_url = '/api/1.0/'

    user1 = {'username': 'test', 'password': u'asdasd'}
    user2 = {'username': 'test-user-2', 'password': u'test-password-2'}

    def setUp(self):
        """
        Here we set up our test objects for the tests
        """
        self.user_obj = User.objects.create_user(
            self.user1['username'], "asd@asd.se", self.user1['password'])
        self.user_obj2 = User.objects.create_user(
            self.user2['username'], "user@email.com", self.user2['password'])
        self.user_obj2.is_active = False
        self.user_obj2.save()
        self.client_obj = Client.objects.create(
            user=self.user_obj,
            name="clientname",
            url="http://app.com/",
            redirect_uri='http://app.com/?callback',
            client_type=0
        )
        self.client_obj2 = Client.objects.create(
            user=self.user_obj2,
            name="testclient",
            url="http://app.com/",
            redirect_uri='http://app.com/?callback',
            client_type=0
        )

        self.position = Position.objects.create(
            name="Kalmar",
            address="Kalmar, Sweden",
            longitude=56,
            latitude=19
        )

    def get_token(self, user, client):
        """
        Method for getting oauth token
        """
        data = {
            'grant_type': 'password', 'username': user['username'],
            'password': user['password'], 'client_id': client.client_id,
            'client_secret': client.client_secret
        }

        # Post our data to the oauth access point
        response = self.client.post('/oauth2/access_token/', data)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse the content
        response_data = loads(response.content)

        # Check if access_token is in our response_data
        self.assertTrue('access_token' in response_data)

        # Get the token
        token = response_data['access_token']

        # Send it!
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)


class PositionTest(UserAPITestCase):

    """
    API tests for the Positions API
    """

    def test_get_positions_requires_login(self):
        """
        Test method for checking that to get positions
        requires user to be logged in
        """
        # Send request to the positions API
        response = self.client.get('%spositions/' % self.api_url)

        # Check that our response is "Unauthorized"
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check for error message
        self.assertEqual(
            response.data['detail'], "Authentication credentials were not provided.")

    def test_get_positions_as_inactive_cant_get_positions(self):
        """
        Test method for checking that in_active users can not
        get any data
        """
        # Get the access_token
        self.get_token(self.user2, self.client_obj2)

        # Send request to the positions API
        response = self.client.get('%spositions/' % self.api_url)

        # Check that our response is "Unauthorized"
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Check for error message
        self.assertEqual(
            response.data['detail'], "User inactive or deleted: %s" % self.user2["username"])

    def test_can_retrieve_positions(self):
        """
        Test method for checking that authorized users can
        get position data
        """
        # Get our access_token
        self.get_token(self.user1, self.client_obj)

        # Send request to the positions API
        response = self.client.get('%spositions/' % self.api_url)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content)

        # Check that our data is what it should be
        self.assertEqual(response_data[0]['name'], "Kalmar")
        self.assertEqual(response_data[0]['address'], "Kalmar, Sweden")
        self.assertEqual(response_data[0]['longitude'], '56')
        self.assertEqual(response_data[0]['latitude'], '19')
