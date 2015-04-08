# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20150407_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='client_funds_rating',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tasklist',
            name='task_effort_rating',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
