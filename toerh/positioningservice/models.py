from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=128, blank=True)
    address = models.CharField(max_length=200, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    position = models.ForeignKey('positioningservice.Position')
    user = models.ForeignKey('auth.User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
