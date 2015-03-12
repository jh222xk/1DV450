# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import positioningservice.models


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0014_auto_20150304_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffee',
            name='image',
            field=models.ImageField(default='media/pictures/no-image.jpg', upload_to=positioningservice.models.content_file_name),
            preserve_default=True,
        ),
    ]
