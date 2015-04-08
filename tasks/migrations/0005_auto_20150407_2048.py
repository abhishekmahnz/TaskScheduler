# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20150407_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='notes',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='notes_html',
            field=models.TextField(default=b'', editable=False, blank=True),
            preserve_default=True,
        ),
    ]
