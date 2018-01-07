# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-03 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0004_auto_20171024_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentariopedido',
            name='principal',
            field=models.BooleanField(default=False, verbose_name=b'Principal'),
        ),
        migrations.AddField(
            model_name='producto',
            name='destacado',
            field=models.BooleanField(default=False, verbose_name=b'Destacado'),
        ),
        migrations.AddField(
            model_name='producto',
            name='oferta',
            field=models.BooleanField(default=False, verbose_name=b'Oferta'),
        ),
        migrations.AddField(
            model_name='producto',
            name='shop',
            field=models.BooleanField(default=False, verbose_name=b'Shop'),
        ),
    ]
