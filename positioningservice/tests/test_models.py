from django.contrib.auth.models import User

from django.test import TestCase

from ..models import Position, Tag


class PositionModelTest(TestCase):
    def test_string_representation(self):
        position = Position.objects.create(
            longitude=56,
            latitude=19
        )
        self.assertEqual(position.__str__(), "[%i, %i]" %
                         (position.longitude, position.latitude))


class TagModelTest(TestCase):
    def test_string_representation(self):
        self.user_obj = User.objects.create_user('test', "asd@asd.se", 'password')
        tag = Tag.objects.create(
            name='#guldveckan',
            user=self.user_obj
        )
        self.assertEqual(tag.__str__(), tag.name)

    def test_get_absolute_url(self):
        self.user_obj = User.objects.create_user('test', "asd@asd.se", 'password')
        tag = Tag.objects.create(
            name='#guldveckan',
            user=self.user_obj
        )
        self.assertIsNotNone(tag.get_absolute_url())
