# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0002_auto_20150121_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(blank=True, max_length=128),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='position',
            field=models.ForeignKey(to='positioningservice.Position', related_name='events'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='users'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('position', 'user')]),
        ),
    ]
