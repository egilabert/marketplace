# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0007_empresa_own_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='spec_similarity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]