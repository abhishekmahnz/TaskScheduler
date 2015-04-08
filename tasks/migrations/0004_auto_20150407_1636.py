# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20150407_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasklist',
            name='client_funds_rating',
        ),
        migrations.RemoveField(
            model_name='tasklist',
            name='task_effort_rating',
        ),
        migrations.AddField(
            model_name='task',
            name='client_funds_rating',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='task_effort_rating',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
