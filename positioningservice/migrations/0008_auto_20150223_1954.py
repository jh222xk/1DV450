# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0007_remove_review_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='reviews',
            field=models.ManyToManyField(related_name='reviews', to='positioningservice.Review'),
            preserve_default=True,
        ),
    ]
