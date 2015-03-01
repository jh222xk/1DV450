# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0011_tag_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='position',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='event',
            name='user',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.RemoveField(
            model_name='position',
            name='address',
        ),
        migrations.AddField(
            model_name='coffee',
            name='address',
            field=models.CharField(max_length=200, default=1),
            preserve_default=False,
        ),
    ]
