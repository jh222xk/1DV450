import base64
from urllib.parse import urlparse
from json import loads
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from ..models import Position, Event, Tag


class UserAPITestCase(APITestCase):

    """
    Base API test class so we can have logged in user
    """

    user1 = {'username': 'test', 'password': 'asdasd'}

    def setUp(self):
        """
        Here we set up our test objects for the tests
        """
        self.user_obj = User.objects.create_user(
            self.user1['username'], "asd@asd.se", self.user1['password'])

        self.token = Token.objects.create(
            user=self.user_obj
        )

        self.position = Position.objects.create(
            name="Kalmar",
            address="Kalmar, Sweden",
            longitude=56,
            latitude=19
        )

        self.position2 = Position.objects.create(
            name="Stockholm",
            address="Stockholm, Sweden",
            longitude=12.344,
            latitude=39.919
        )

        self.tag1 = Tag.objects.create(
            name='#guldveckan'
        )
        self.tag2 = Tag.objects.create(
            name='#kalmar'
        )

        self.event = Event.objects.create(
            name='Guldveckan Kalmar',
            position=self.position,
            user=self.user_obj,
        )

        self.event.tags.add(self.tag1, self.tag2)

        self.event2 = Event.objects.create(
            name='DjangoCon Europe',
            position=self.position2,
            user=self.user_obj
        )

    def tearDown(self):
        self.user_obj.delete()
        self.token.delete()
        self.position.delete()

    def get_token(self, user):
        """
        Method for getting JSONWebTokenAuthentication
        """
        data = {
            'username': user['username'],
            'password': user['password']
        }

        # Post our data to the oauth access point
        response = self.client.post(reverse('token-auth'), data)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse the content
        response_data = loads(response.content.decode("utf-8"))

        # Check if access_token is in our response_data
        self.assertTrue('token' in response_data)

        # Get the token
        token = response_data['token']

        return token


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
        response = self.client.get(reverse('api-v1:position-list'))

        # Check that our response is "Unauthorized"
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check for error message
        self.assertEqual(
            response.data['detail'], "Authentication credentials were not provided.")

    def test_get_positions_requires_not_only_token_header(self):
        """
        Test method for checking that to get positions
        requires user to be logged in
        """
        # Send request to the positions API
        response = self.client.get(
            reverse('api-v1:position-list'), {}, HTTP_AUTHORIZATION='JWT')

        # Check that our response is "Unauthorized"
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check for error message
        self.assertEqual(
            response.data['detail'], "Invalid Authorization header. No credentials provided.")

    def test_get_positions_requires_a_valid_account(self):
        """
        Test method for checking that to get positions
        requires user to be logged in
        """
        # Send request to the positions API
        response = self.client.get(
            reverse('api-v1:position-list'), {}, HTTP_AUTHORIZATION='JWT 123a39394')

        # Check that our response is "Unauthorized"
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check for error message
        self.assertEqual(
            response.data['detail'], "Error decoding signature.")

    def test_can_retrieve_positions(self):
        """
        Test method for checking that authorized users can
        get a list of positions
        """

        # Get our access_token
        token = self.get_token(self.user1)

        # Send request to the positions API
        response = self.client.get(
            reverse('api-v1:position-list'), {}, HTTP_AUTHORIZATION='JWT %s' % token)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content.decode('utf-8'))

        # Check that our data is what it should be
        self.assertEqual(response_data['results'][0]['name'], "Kalmar")
        self.assertEqual(
            response_data['results'][0]['address'], "Kalmar, Sweden")
        self.assertEqual(response_data['results'][0]['longitude'], '56.000')
        self.assertEqual(response_data['results'][0]['latitude'], '19.000')
        self.assertEqual(response_data['results'][1]['name'], "Stockholm")
        self.assertEqual(
            response_data['results'][1]['address'], "Stockholm, Sweden")
        self.assertEqual(response_data['results'][1]['longitude'], '12.344')
        self.assertEqual(response_data['results'][1]['latitude'], '39.919')

        # Check events
        self.assertEqual(
            response_data['results'][0]['events'][0]['name'], "Guldveckan Kalmar")

    def test_can_retrieve_a_single_position(self):
        """
        Test for checking that authorized users can
        get a SINGLE position
        """

        # Get our access_token
        token = self.get_token(self.user1)

        # Send request to the positions API
        response = self.client.get(reverse(
            'api-v1:position-detail', kwargs={'pk': 1}), {}, HTTP_AUTHORIZATION='JWT %s' % token)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content.decode('utf-8'))

        # Check that our data is what it should be
        self.assertEqual(response_data['name'], "Kalmar")
        self.assertEqual(response_data['address'], "Kalmar, Sweden")
        self.assertEqual(response_data['longitude'], '56.000')
        self.assertEqual(response_data['latitude'], '19.000')

        # Send a new request to the positions API to get pk id 2
        response = self.client.get(reverse(
            'api-v1:position-detail', kwargs={'pk': 2}), {}, HTTP_AUTHORIZATION='JWT %s' % token)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content.decode('utf-8'))

        # Check that our data is what it should be
        self.assertEqual(response_data['name'], "Stockholm")
        self.assertEqual(response_data['address'], "Stockholm, Sweden")
        self.assertEqual(response_data['longitude'], '12.344')
        self.assertEqual(response_data['latitude'], '39.919')

        # Check events
        self.assertEqual(
            response_data['events'][0]['name'], "DjangoCon Europe")


class EventTest(UserAPITestCase):

    """
    API tests for the Events API
    """

    def test_can_retrieve_events(self):
        """
        Test method for checking that authorized users can
        get a list of events
        """

        # Get our access_token
        token = self.get_token(self.user1)

        # Send request to the positions API
        response = self.client.get(
            reverse('api-v1:event-list'), {}, HTTP_AUTHORIZATION='JWT %s' % token)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content.decode('utf-8'))

        # Check that our data is what it should be
        self.assertEqual(
            response_data['results'][0]['name'], "Guldveckan Kalmar")

    def test_can_retrieve_a_single_event(self):
        """
        Test for checking that authorized users can
        get a SINGLE event
        """

        # Get our access_token
        token = self.get_token(self.user1)

        # Send request to the positions API
        response = self.client.get(reverse(
            'api-v1:event-detail', kwargs={'pk': 1}), {}, HTTP_AUTHORIZATION='JWT %s' % token)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content.decode('utf-8'))

        # Check that our data is what it should be
        self.assertEqual(response_data['name'], "Guldveckan Kalmar")
        self.assertEqual(
            urlparse(response_data['url']).path, reverse('api-v1:event-detail', kwargs={'pk': 1}))

        # First tag
        self.assertEqual(response_data['tags'][0]['name'], "#guldveckan")
        self.assertEqual(urlparse(response_data['tags'][0]['url']).path, reverse(
            'api-v1:tag-detail', kwargs={'pk': 1}))

        # Second tag
        self.assertEqual(response_data['tags'][1]['name'], "#kalmar")
        self.assertEqual(urlparse(response_data['tags'][1]['url']).path, reverse(
            'api-v1:tag-detail', kwargs={'pk': 2}))


class TagTest(UserAPITestCase):

    """
    API tests for the Tag API
    """

    def test_can_retrieve_tags(self):
        """
        Test method for checking that authorized users can
        get a list of tags
        """

        # Get our access_token
        token = self.get_token(self.user1)

        # Send request to the positions API
        response = self.client.get(
            reverse('api-v1:tag-list'), {}, HTTP_AUTHORIZATION='JWT %s' % token)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content.decode('utf-8'))

        # Check that our data is what it should be
        self.assertEqual(
            response_data['results'][0]['name'], "#guldveckan")
        self.assertEqual(
            response_data['results'][1]['name'], "#kalmar")


    def test_can_retrieve_a_single_tag(self):
        """
        Test for checking that authorized users can
        get a SINGLE tag
        """

        # Get our access_token
        token = self.get_token(self.user1)

        # Send request to the positions API
        response = self.client.get(reverse(
            'api-v1:tag-detail', kwargs={'pk': 1}), {}, HTTP_AUTHORIZATION='JWT %s' % token)

        # Check that our response is fine
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Parse our response
        response_data = loads(response.content.decode('utf-8'))

        # Check that our data is what it should be
        self.assertEqual(response_data['name'], "#guldveckan")
        self.assertEqual(
            urlparse(response_data['url']).path, reverse('api-v1:tag-detail', kwargs={'pk': 1}))
