# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 14:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0004_auto_20161229_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cirbe',
            name='corto_plazo_concedido',
        ),
    ]
