import urllib
import json
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.contrib.gis.geos import Point
from django.db.models import Avg
from django.db.models.signals import post_save

from .signals import update_index


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Position(models.Model):
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[%s, %s]" % (self.longitude, self.latitude)

    @property
    def geo_location(self):
        return Point(self.latitude, self.longitude)


class Tag(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('api-v1:tag-detail', kwargs={'pk': self.id})


class Coffee(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=200)
    position = models.ForeignKey(Position)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Creates a position bonded to a coffeehouse
        Creates only on coffee-creation.
        """
        if self.pk is None:
            geo = json.loads(self.get_lat_lon(self.address))
            position = Position()
            if geo['status'] == "OK":
                position.latitude = geo['results'][0]['geometry']['location']['lat']
                position.longitude = geo['results'][0]['geometry']['location']['lng']
            position.save()
            self.position = position
        super().save(*args, **kwargs)

    def get_lat_lon(self, address):
        """
        Fetches the latitude and longitude from an address
        from Google's API
        """
        address = urllib.parse.quote_plus(address)
        geo = urllib.request.urlopen(
            "https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % address)
        return geo.readall().decode('utf-8')

    def get_location(self):
        return Point(self.position.latitude, self.position.longitude)

    @property
    def rating(self):
        """
        Rating calculated from all the reviews
        for this coffeehouse
        """
        average = self.review.all().aggregate(Avg('rating'))['rating__avg']
        if not average:
            return 0
        return average


class Review(models.Model):
    rating = models.FloatField()
    coffee = models.ForeignKey(Coffee, related_name='review')
    description = models.TextField()
    user = models.ForeignKey(AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.rating

# Update our indexes when a new coffeehouse is created
post_save.connect(update_index, sender=Coffee)