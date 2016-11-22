from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Empresa(models.Model):
    fiscal_id = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    data_date = models.DateField()
    creation_date = models.DateField()
    sector = models.CharField(max_length=255)
    cnae = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    hats_date = models.DateField()
    hats_alert = models.CharField(max_length=30)
    concursal = models.CharField(max_length=10)
    recent_creation = models.CharField(max_length=10)
    segment = models.CharField(max_length=128)
    subsegment = models.CharField(max_length=128)
    territorial = models.CharField(max_length=255)
    regional = models.CharField(max_length=255)
    centro_gestor = models.CharField(max_length=255)
    oficina = models.IntegerField()
    
    def __str__(self):              # __unicode__ on Python 2
        return self.name
