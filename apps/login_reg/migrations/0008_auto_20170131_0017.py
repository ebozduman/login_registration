# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 00:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0007_auto_20170130_2357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='favorites',
            new_name='quotes',
        ),
    ]