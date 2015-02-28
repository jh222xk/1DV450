# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0008_auto_20150223_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffee',
            name='reviews',
        ),
        migrations.AddField(
            model_name='review',
            name='coffee',
            field=models.ForeignKey(to='positioningservice.Coffee', default=1),
            preserve_default=False,
        ),
    ]
