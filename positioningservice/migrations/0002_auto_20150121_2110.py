# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('positioningservice', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Creator',
        ),
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 9, 30, 262369, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='position',
            field=models.ForeignKey(default=1, to='positioningservice.Position'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 9, 57, 356463, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 10, 6, 827356, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 10, 13, 155105, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 10, 18, 634825, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 10, 22, 674302, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
