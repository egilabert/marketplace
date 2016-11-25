from __future__ import unicode_literals
import numpy as np
from django.db import models

# Create your models here.
class Empresa(models.Model):

    fiscal_id = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    data_date = models.DateField(null=True)
    creation_date = models.DateField(null=True)
    sector = models.CharField(max_length=255)
    cnae = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255)
    hats_date = models.DateField(null=True)
    hats_alert = models.CharField(max_length=30)
    concursal = models.CharField(max_length=10)
    recent_creation = models.CharField(max_length=10)
    segment = models.CharField(max_length=128)
    subsegment = models.CharField(max_length=128)
    territorial = models.CharField(max_length=255)
    regional = models.CharField(max_length=255)
    centro_gestor = models.CharField(max_length=255)
    oficina = models.IntegerField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def average_transfer(self):
        all_transfers = map(lambda x: x.amount, self.origin_reference.all())
        return np.mean(all_transfers)
    
    def __unicode__(self):
        return self.name

class Transfer(models.Model):

    origin_reference = models.ForeignKey(Empresa, related_name='origin_reference', on_delete=models.CASCADE)
    concept = models.CharField(max_length=255)
    operation_data = models.DateTimeField()
    value_date = models.DateTimeField()
    amount = models.IntegerField()
    balance = models.IntegerField()
    destination_reference = models.ForeignKey(Empresa, related_name='destination_reference', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.concept

class RecommendedClients(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='empresa', on_delete=models.CASCADE)
    similarity = models.FloatField()
    clientes_recomendados = models.ForeignKey(Empresa, related_name='clientes_recomendados', on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.similarity)
