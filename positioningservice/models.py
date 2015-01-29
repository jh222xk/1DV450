from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=6, decimal_places=3)
    latitude = models.DecimalField(max_digits=6, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s (%s,%s)" % (self.name, self.longitude, self.latitude)


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