# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-18 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20170918_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follows_list',
            field=models.ManyToManyField(related_name='follows', to='user.Profile'),
        ),
    ]
