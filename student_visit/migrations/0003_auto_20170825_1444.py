# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_visit', '0002_auto_20170822_0840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reason',
            options={'ordering': ('ordering', '-term', 'verbose_name')},
        ),
        migrations.AlterModelOptions(
            name='studentvisit',
            options={'ordering': ('-when', )},
        ),
        migrations.AddField(
            model_name='studentvisit',
            name='agree',
            field=models.BooleanField(default=False),
        ),
    ]