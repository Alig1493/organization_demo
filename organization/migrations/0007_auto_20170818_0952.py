# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 09:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20170818_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='updated_by',
        ),
    ]
