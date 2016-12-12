# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0012_auto_20161130_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='dias_impago',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='productos',
            name='fecha_datos',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='productos',
            name='segmento_gestion',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='estadosfinancieros',
            name='ejercicio',
            field=models.CharField(max_length=16, null=True),
        ),
    ]