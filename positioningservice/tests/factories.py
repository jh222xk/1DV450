import faker
from factory import DjangoModelFactory, lazy_attribute, SubFactory, post_generation

from ..models import Position, Event, Tag


faker = faker.Factory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)

    first_name = lazy_attribute(lambda o: faker.first_name())
    last_name = lazy_attribute(lambda o: faker.last_name())
    username = lazy_attribute(lambda o: faker.user_name())
    email = lazy_attribute(lambda o: faker.email())


class PositionFactory(DjangoModelFactory):
    class Meta:
        model = Position

    name = lazy_attribute(lambda o: faker.city())
    address = lazy_attribute(lambda o: faker.address())
    latitude = lazy_attribute(lambda o: faker.latitude())
    longitude = lazy_attribute(lambda o: faker.longitude())
    created_at = lazy_attribute(lambda o: faker.date_time())
    updated_at = lazy_attribute(lambda o: faker.date_time())


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = lazy_attribute(lambda o: "#%s" % faker.name())


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = lazy_attribute(lambda o: faker.name())
    position = SubFactory(PositionFactory)
    user = SubFactory(UserFactory)

    @post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
