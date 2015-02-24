from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.contrib.gis.geos import Point
from django.db.models import Avg


class Position(models.Model):
    #name = models.CharField(max_length=128)
    address = models.CharField(max_length=200)
    longitude = models.FloatField()
    latitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s (%s, %s)" % (self.name, self.longitude, self.latitude)


    @property
    def geo_location(self):
        return Point(self.latitude, self.longitude)


class Coffee(models.Model):
    name = models.CharField(max_length=128)
    position = models.ForeignKey(Position)
    #reviews = models.ManyToManyField('positioningservice.Review', related_name='coffeehouses')
    tags = models.ManyToManyField('positioningservice.Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_location(self):
        return Point(self.position.latitude, self.position.longitude)

    @property
    def rating(self):
        average = self.review.all().aggregate(Avg('rating'))['rating__avg']
        if not average:
            return 0
        return average


class Review(models.Model):
    rating = models.FloatField()
    coffee = models.ForeignKey(Coffee, related_name='review')
    description = models.TextField()
    user = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.rating


class Event(models.Model):
    name = models.CharField(max_length=128)
    position = models.ForeignKey('positioningservice.Position', related_name='events')
    tags = models.ManyToManyField('positioningservice.Tag')
    user = models.ForeignKey('auth.User', related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('api-v1:tag-detail', kwargs={'pk': self.id})