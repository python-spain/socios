# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0004_auto_20161016_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuota',
            name='fecha',
            field=models.DateField(blank=True),
        ),
    ]
