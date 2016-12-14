from __future__ import unicode_literals
import numpy as np
from django.db import models
from  django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Avg, Max, Min, Count, Sum
from django.db.models.functions import TruncMonth

# ------------------------------------------------------------------
# Model Empresa
# Tabla y funciones del model Empresa
# ------------------------------------------------------------------
class Empresa(models.Model):

    fiscal_id = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    data_date = models.DateField(null=True, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    sector = models.CharField(max_length=255)
    cnae = models.CharField(max_length=255)
    cnae_2 = models.CharField(max_length=255, blank=True, null=True)
    cnae_num = models.IntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=255)
    hats_date = models.DateField(null=True, blank=True)
    hats_alert = models.CharField(max_length=30)
    concursal = models.CharField(max_length=10)
    recent_creation = models.CharField(max_length=10)
    segment = models.CharField(max_length=128)
    subsegment = models.CharField(max_length=128)
    territorial = models.CharField(max_length=255)
    regional = models.CharField(max_length=255)
    centro_gestor = models.CharField(max_length=255)
    oficina = models.IntegerField()
    state_name = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    clients = models.ManyToManyField("self", blank=True)
    providers = models.ManyToManyField("self", blank=True)
    recommended_clients = models.ManyToManyField("self", blank=True)
    recommended_providers = models.ManyToManyField("self", blank=True)
    oportunities = models.ManyToManyField("self", blank=True)

    # Helper functions of the model empresaas 

    def average_transfer_to_provider(self):
        all_transfers = map(lambda x: x.amount, self.transfers.all())
        return np.mean(all_transfers)

    def average_transfer_from_client(self):
        all_transfers = map(lambda x: x.amount, self.destination_reference.all())
        return np.mean(all_transfers)

    def get_clients(self):
        return Empresa.objects.filter(transfers__destination_reference=self).annotate(Count('name', distinct=True))

    def get_qs_clients(self,qs):
        return Empresa.objects.filter(transfers__destination_reference__in=qs).annotate(Count('name', distinct=True))

    def get_providers(self):
        return Empresa.objects.filter(destination_reference__in=Transfer.objects.filter(origin_reference=self)).annotate(Count('name', distinct=True))

    def get_qs_providers(self,qs):
        return Empresa.objects.filter(destination_reference__in=Transfer.objects.filter(origin_reference__in=qs)).annotate(Count('name', distinct=True))

    def in_my_region(self, qs):
        return qs.filter(territorial=self.territorial)

    def get_monthly_buys(self):
        group_by = self.transfers.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('-month')
        return group_by

    def get_monthly_sells(self):
        group_by = self.destination_reference.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('-month')
        return group_by

    def get_monthly_buys_amount(self):
        group_by = self.transfers.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('-month')
        return group_by

    def get_monthly_sells_amount(self):
        group_by = self.destination_reference.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('-month')
        return group_by

    def get_total_buys(self):
        total = self.transfers.all().aggregate(total=Sum('amount'))
        return total

    def get_total_sells(self):
        total = self.destination_reference.all().aggregate(total=Sum('amount'))
        return total

    def get_total_sector_buys(self):
        total = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).aggregate(total=Sum('amount'))
        return total

    def get_total_sector_sells(self):
        total = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).aggregate(total=Sum('amount'))
        return total

    def get_sectors(self, qs):
        group_by = qs.values("cnae_2").annotate(count=Count('id', distinct=True)).order_by('-count')
        sectores = [d['cnae_2'] for d in group_by]
        counts = [d['count'] for d in group_by]
        return sectores, counts

    def out_of_my_region(self, qs):
        return qs.exclude(territorial=self.territorial)

    def get_sector_companies(self):
        return Empresa.objects.filter(cnae=self.cnae)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("empresas:detail", kwargs={"pk": self.id})


# ------------------------------------------------------------------
# Model Transfer
# Tabla y funciones del model Transfer (transferencias entre empresas)
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# Model EstadosFinancieros
# Tabla y funciones del model EstadosFinancieros (de una empresa)
# ------------------------------------------------------------------
class EstadosFinancieros(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='estados_financieros', null=True, blank=True, on_delete=models.CASCADE)
    ejercicio = models.CharField(max_length=16, null=True, blank=True)
    fecha_balance = models.DateField(null=True, blank=True)
    ventas = models.FloatField(null=True, blank=True)
    depreciaciones = models.FloatField(null=True, blank=True)
    amortizaciones = models.FloatField(null=True, blank=True)
    ebitda = models.FloatField(null=True, blank=True)
    resultado_explotacion = models.FloatField(null=True, blank=True)
    existencias = models.FloatField(null=True, blank=True)
    deudores = models.FloatField(null=True, blank=True)
    periodificaciones_ac = models.FloatField(null=True, blank=True)
    provisiones_cp = models.FloatField(null=True, blank=True)
    acreedores_comerciales = models.FloatField(null=True, blank=True)
    periodificaciones_pc = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.ejercicio or u''

# ------------------------------------------------------------------
# Model Productos
# Tabla y funciones del model Productos (contratados por una empresa)
# ------------------------------------------------------------------
class Productos(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='productos', on_delete=models.CASCADE)
    numero_persona = models.IntegerField(null=True, blank=True)
    tipo_producto = models.CharField(max_length=5, null=True, blank=True)
    producto = models.CharField(max_length=128, null=True, blank=True)
    desc_producto = models.CharField(max_length=128, null=True, blank=True)
    id_contrato = models.CharField(max_length=32, null=True, blank=True)
    concedido = models.FloatField(null=True, blank=True)
    dispuesto = models.FloatField(null=True, blank=True)
    impagado = models.FloatField(null=True, blank=True)
    dias_impago = models.FloatField(null=True, blank=True)
    cuotas_impagadas = models.FloatField(null=True, blank=True)
    fecha_datos = models.DateField(null=True, blank=True)
    fecha_formalizacion = models.DateField(null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    concedido_inicial = models.FloatField(null=True, blank=True)
    capital_pdte = models.FloatField(null=True, blank=True)
    interes_revisado = models.FloatField(null=True, blank=True)
    cuotas_total = models.FloatField(null=True, blank=True)
    cuota_anual = models.FloatField(null=True, blank=True)
    cuota = models.FloatField(null=True, blank=True)
    garantia_hip = models.CharField(max_length=2, null=True, blank=True)
    sit_contable = models.CharField(max_length=32, null=True, blank=True)
    segmento_gestion = models.CharField(max_length=128, null=True, blank=True)
    refinanciado = models.BooleanField()

    def __unicode__(self):
        return self.tipo_producto

# ------------------------------------------------------------------
# Model RecommendedClients
# Tabla y funciones del model RecommendedClients (recommendaciones entre empresa)
# ------------------------------------------------------------------
class RecommendedClients(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='recommended', on_delete=models.CASCADE)
    similarity = models.FloatField()
    clientes_recomendados = models.ForeignKey(Empresa, related_name='clientes_recomendados', on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.similarity)

    class Meta:
        ordering = ['-similarity']

# ------------------------------------------------------------------
# Model RecommendedProviders
# Tabla y funciones del model RecommendedProviders (recommendaciones entre empresa)
# ------------------------------------------------------------------
class RecommendedProviders(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='providers_recommended', on_delete=models.CASCADE)
    similarity = models.FloatField()
    clientes_recomendados = models.ForeignKey(Empresa, related_name='proveedores_recomendados', on_delete=models.CASCADE)

    def __unicode__(self):
        return str(self.similarity)

    class Meta:
        ordering = ['-similarity']
