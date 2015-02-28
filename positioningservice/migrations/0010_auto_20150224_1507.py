# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0009_auto_20150224_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='name',
        ),
        migrations.AlterField(
            model_name='review',
            name='coffee',
            field=models.ForeignKey(related_name='review', to='positioningservice.Coffee'),
            preserve_default=True,
        ),
    ]
