# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sector', models.CharField(max_length=255)),
                ('antiguedad', models.CharField(max_length=255)),
                ('fondos_propios', models.IntegerField()),
                ('patrimonio', models.IntegerField()),
                ('activo_corriente', models.IntegerField()),
                ('activo_no_corriente', models.IntegerField()),
                ('pasivo_corriente', models.IntegerField()),
                ('pasivo_no_corriente', models.IntegerField()),
                ('importe_neto_cifra_negocio', models.IntegerField()),
                ('gastos_financieros', models.IntegerField()),
                ('resultados_antes_impuestos', models.IntegerField()),
            ],
        ),
    ]
