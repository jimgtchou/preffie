# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-17 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='follows_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Profile'),
        ),
    ]
