# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-17 22:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0003_auto_20170917_0349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='user_vote',
        ),
    ]
