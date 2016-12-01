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
        all_transfers = map(lambda x: x.amount, self.transfers.all())
        return np.mean(all_transfers)
    
    def __unicode__(self):
        return self.name

class Transfer(models.Model):

    origin_reference = models.ForeignKey(Empresa, related_name='transfers', on_delete=models.CASCADE)
    concept = models.CharField(max_length=255)
    operation_data = models.DateTimeField()
    value_date = models.DateTimeField()
    amount = models.IntegerField()
    balance = models.IntegerField()
    destination_reference = models.ForeignKey(Empresa, related_name='destination_reference', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.concept

class EstadosFinancieros(models.Model):

    try:
        empresa = models.ForeignKey(Empresa, related_name='estados_financieros', null=True, on_delete=models.CASCADE)
        ejercicio = models.CharField(max_length=16, null=True)
        fecha_balance = models.DateField(null=True)
        ventas = models.FloatField(null=True)
        depreciaciones = models.FloatField(null=True)
        amortizaciones = models.FloatField(null=True)
        ebitda = models.FloatField(null=True)
        resultado_explotacion = models.FloatField(null=True)
        existencias = models.FloatField(null=True)
        deudores = models.FloatField(null=True)
        periodificaciones_ac = models.FloatField(null=True)
        provisiones_cp = models.FloatField(null=True)
        acreedores_comerciales = models.FloatField(null=True)
        periodificaciones_pc = models.FloatField(null=True)
        created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    except:
        pass

    def __unicode__(self):
        return self.ejercicio or u''

class Productos(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='productos', on_delete=models.CASCADE)
    numero_persona = models.IntegerField(null=True)
    tipo_producto = models.CharField(max_length=5, null=True)
    producto = models.CharField(max_length=128, null=True)
    desc_producto = models.CharField(max_length=128, null=True)
    id_contrato = models.CharField(max_length=32, null=True)
    concedido = models.FloatField(null=True)
    dispuesto = models.FloatField(null=True)
    impagado = models.FloatField(null=True)
    dias_impago = models.FloatField(null=True)
    cuotas_impagadas = models.FloatField(null=True)
    fecha_datos = models.DateField(null=True)
    fecha_formalizacion = models.DateField(null=True)
    fecha_vencimiento = models.DateField(null=True)
    concedido_inicial = models.FloatField(null=True)
    capital_pdte = models.FloatField(null=True)
    interes_revisado = models.FloatField(null=True)
    cuotas_total = models.FloatField(null=True)
    cuota_anual = models.FloatField(null=True)
    cuota = models.FloatField(null=True)
    garantia_hip = models.CharField(max_length=2, null=True)
    sit_contable = models.CharField(max_length=32, null=True)
    segmento_gestion = models.CharField(max_length=128, null=True)
    refinanciado = models.BooleanField()

    def __unicode__(self):
        return self.tipo_producto


class RecommendedClients(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='empresa', on_delete=models.CASCADE)
    similarity = models.FloatField()
    clientes_recomendados = models.ForeignKey(Empresa, related_name='clientes_recomendados', on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.similarity)
