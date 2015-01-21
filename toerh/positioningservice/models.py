from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=128, blank=True)
    address =models.CharField(max_length=200, blank=True)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    latitude = models.DecimalField(max_digits=6, decimal_places=3)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    pass


class Tag(models.Model):
    pass


class Creator(models.Model):
    pass