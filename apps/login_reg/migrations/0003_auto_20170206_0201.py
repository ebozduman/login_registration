# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0002_auto_20170206_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='date',
            field=models.DateField(blank=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='time',
            field=models.TimeField(blank=True, default=None),
            preserve_default=False,
        ),
    ]
