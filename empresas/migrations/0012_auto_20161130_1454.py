# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 14:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0011_auto_20161129_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadosfinancieros',
            name='empresa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='empresas.Empresa'),
        ),
    ]