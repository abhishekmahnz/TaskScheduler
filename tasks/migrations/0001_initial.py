# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('user', models.ForeignKey(related_name='lists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'order_date',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tasklist',
            unique_together=set([('user', 'name')]),
        ),
    ]
