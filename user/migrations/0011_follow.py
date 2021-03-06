# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-23 18:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0010_remove_profile_follows_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('follows', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_follows', to='user.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relationship', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
