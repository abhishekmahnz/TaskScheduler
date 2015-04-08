# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('when_Deadline', models.DateTimeField()),
                ('client', models.CharField(max_length=10, choices=[(b'Manager', b'Manager'), (b'VPD', b'VPD'), (b'R&D', b'R&D Dept.')])),
                ('supervisor', models.CharField(max_length=255)),
                ('task_list', models.ForeignKey(related_name='tasks', to='tasks.TaskList')),
            ],
            options={
                'ordering': ('when_Deadline', 'client'),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('task_list', 'name')]),
        ),
    ]
