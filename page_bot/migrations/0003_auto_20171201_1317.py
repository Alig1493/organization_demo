# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-01 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page_bot', '0002_auto_20171130_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagevaluemodel',
            name='post_id',
            field=models.CharField(max_length=1000),
        ),
    ]