import binascii
import os
from django.conf import settings

from django.db import models

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key