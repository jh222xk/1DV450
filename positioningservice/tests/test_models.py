from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Position, Event, Tag


class PositionModelTest(TestCase):

    def test_string_representation(self):
        position = Position.objects.create(
            name="Kalmar",
            address="Kalmar, Sweden",
            longitude=56,
            latitude=19
        )
        self.assertEqual(position.__str__(), "%s (%i, %i)" %
                         (position.name, position.longitude, position.latitude))


class EventModelTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(
            name="Kalmar",
            address="Kalmar, Sweden",
            longitude=56,
            latitude=19
        )
        self.user = User.objects.create_user(
            'test-user', 'test@mail.com', 'test-password')

    def tearDown(self):
        self.position.delete()
        self.user.delete()

    def test_string_representation(self):
        event = Event.objects.create(
            name='Guldveckan Kalmar',
            position=self.position,
            user=self.user,
        )
        self.assertEqual(event.__str__(), event.name)


class TagModelTest(TestCase):

    def test_string_representation(self):
        tag = Tag.objects.create(
            name='#guldveckan'
        )
        self.assertEqual(tag.__str__(), tag.name)


    def test_get_absolute_url(self):
        tag = Tag.objects.create(
            name='#guldveckan'
        )
        self.assertIsNotNone(tag.get_absolute_url())
