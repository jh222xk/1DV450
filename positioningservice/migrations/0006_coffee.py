# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('positioningservice', '0005_auto_20150222_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coffee',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.ForeignKey(to='positioningservice.Position')),
                ('reviews', models.ManyToManyField(to='positioningservice.Review')),
                ('tags', models.ManyToManyField(to='positioningservice.Tag')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
