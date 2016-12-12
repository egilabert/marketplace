# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-07 17:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0019_empresa_contact_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedProviders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity', models.FloatField()),
                ('clientes_recomendados', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proveedores_recomendados', to='empresas.Empresa')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='providers_recommended', to='empresas.Empresa')),
            ],
            options={
                'ordering': ['-similarity'],
            },
        ),
    ]