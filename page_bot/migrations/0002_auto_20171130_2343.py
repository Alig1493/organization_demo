# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-30 23:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageFromModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sender_id', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='pageentrymodel',
            old_name='page_id',
            new_name='recipient_id',
        ),
        migrations.RenameField(
            model_name='pagevaluemodel',
            old_name='recipient_id',
            new_name='published',
        ),
        migrations.RemoveField(
            model_name='pagevaluemodel',
            name='sender_id',
        ),
        migrations.RemoveField(
            model_name='pagevaluemodel',
            name='sender_name',
        ),
        migrations.AddField(
            model_name='pagefrommodel',
            name='value',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='page_bot.PageValueModel'),
        ),
    ]