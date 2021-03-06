# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-16 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libro', '0005_auto_20161016_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='socio',
            name='cargo',
            field=models.CharField(choices=[('-', 'Ninguno'), ('P', 'Presidente'), ('V', 'Vicepresidente'), ('T', 'Tesorero'), ('S', 'Secretario'), ('O', 'Vocal')], default='-', max_length=1),
        ),
        migrations.AlterField(
            model_name='socio',
            name='fecha',
            field=models.DateField(blank=True, help_text='Fecha solicitud', null=True),
        ),
    ]
