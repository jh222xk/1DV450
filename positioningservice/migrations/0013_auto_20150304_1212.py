# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0012_auto_20150301_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='coffee',
            name='description',
            field=models.TextField(default='Café med hembakta bakverk i lummig trädgård i Gamla Stan. Sommaröppet maj - september. Endast utomhuscafé.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='position',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='position',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
