# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0006_coffee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='position',
        ),
    ]
