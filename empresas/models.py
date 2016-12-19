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

    # Helpers de los estados financieros
    # ------------------------------------------------------------------

    def annual_balance_exercises(self):
        return self.estados_financieros.all().values('ejercicio').order_by('ejercicio')

    def annual_sector_balance_exercises(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').distinct().order_by('ejercicio')

    def resultado_explotacion(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('resultado_explotacion')).order_by('ejercicio')

    def resultado_explotacion_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_clients_resultado(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_clients()).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_clients_resultado_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=Empresa.objects.filter(transfers__destination_reference__in=self.get_sector_companies())).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_clients_sells(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_clients()).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')

    def balance_clients_sells_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=Empresa.objects.filter(transfers__destination_reference__in=self.get_sector_companies())).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')

    def balance_sells(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('ventas')).order_by('ejercicio')

    def balance_sells_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')

    def balance_depreciation(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('depreciaciones')).order_by('ejercicio')

    def balance_depreciation_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Avg('depreciaciones')).order_by('ejercicio')

    def balance_amortisation(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('amortizaciones')).order_by('ejercicio')

    def balance_amortisation_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Avg('amortizaciones')).order_by('ejercicio')

    def balance_ebitda(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('ebitda')).order_by('ejercicio')

    def balance_ebitda_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')
    
    def balance_clients_ebitda(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_clients()).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')

    def balance_clients_ebitda_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=Empresa.objects.filter(transfers__destination_reference__in=self.get_sector_companies())).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')

    def balance_stock(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('existencias')).order_by('ejercicio')

    def balance_stock_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Avg('existencias')).order_by('ejercicio')

    def balance_debt(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('deudores')).order_by('ejercicio')

    def balance_debt_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Avg('deudores')).order_by('ejercicio')

    def ebitda(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('ebitda')).order_by('ejercicio')

    def ebitda_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').annotate(c=Sum('ebitda')).order_by('ejercicio')

    # Helpers de transferencias
    # ------------------------------------------------------------------

    def average_transfer_to_provider(self):
        group_by = self.transfers.all().aggregate(avg=Avg('amount'))
        return group_by['avg']

    def average_transfer_from_client(self):
        group_by = self.destination_reference.all().aggregate(avg=Avg('amount'))
        return group_by['avg']

    def get_clients(self):
        return Empresa.objects.filter(transfers__destination_reference=self).annotate(Count('name', distinct=True))

    def get_sector_clients(self):
        return Empresa.objects.filter(transfers__destination_reference__in=self.get_sector_companies()).annotate(Count('name', distinct=True)).count()

    def get_providers(self):
        return Empresa.objects.filter(destination_reference__in=Transfer.objects.filter(origin_reference=self)).annotate(Count('name', distinct=True))

    def get_monthly_buys(self):
        group_by = self.transfers.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('month')
        for month in group_by:
            month['month'] = month['month'].strftime("%b %Y")
        return group_by

    def get_monthly_sells(self):
        group_by = self.destination_reference.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('month')
        for month in group_by:
            month['month'] = month['month'].strftime("%b %Y") 
        return group_by

    def get_monthly_sector_avg_sells(self):
        group_by = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('month')
        for month in group_by:
            month['c'] = month['c']/self.get_sector_companies().count()
            month['month'] = month['month'].strftime("%b %Y")
        return group_by

    def get_monthly_buys_amount(self):
        group_by = self.transfers.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('month')
        return group_by

    def get_monthly_sells_amount(self):
        group_by = self.destination_reference.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('month')
        return group_by

    def get_total_buys(self):
        total = self.transfers.all().aggregate(total=Sum('amount'))
        return total['total']

    def get_total_sells(self):
        total = self.destination_reference.all().aggregate(total=Sum('amount'))
        return total['total']

    def get_total_sector_buys(self):
        total = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).aggregate(total=Sum('amount'))
        return total['total']

    def average_sector_buys(self):
        total = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).aggregate(total=Avg('amount'))
        return total['total']

    def get_total_sector_sells(self):
        total = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).aggregate(total=Sum('amount'))
        return total['total']

    def average_sector_sells(self):
        total = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).aggregate(total=Avg('amount'))
        return total['total']

    def get_sector_avg_monthly_sells_amount(self):
        group_by = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Avg('amount')).order_by('month')
        return group_by

    def get_sector_avg_monthly_buys_amount(self):
        group_by = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Avg('amount')).order_by('month')
        return group_by

    def get_sector_total_monthly_sells_amount(self):
        group_by = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('month')
        return group_by

    def get_sector_total_monthly_buys_amount(self):
        group_by = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('month')
        return group_by

    def get_qs_clients(self,qs):
        return Empresa.objects.filter(transfers__destination_reference__in=qs).annotate(Count('name', distinct=True))

    def get_qs_providers(self,qs):
        return Empresa.objects.filter(destination_reference__in=Transfer.objects.filter(origin_reference__in=qs)).annotate(Count('name', distinct=True))

    # General Helpers
    # ------------------------------------------------------------------

    def get_sectors(self, qs):
        group_by = qs.values("cnae_2").annotate(count=Count('id', distinct=True)).order_by('-count')
        sectores = [d['cnae_2'] for d in group_by]
        counts = [d['count'] for d in group_by]
        return sectores, counts

    def out_of_my_region(self, qs):
        return qs.exclude(territorial=self.territorial)

    def in_my_region(self, qs):
        return qs.filter(territorial=self.territorial)

    def get_sector_companies(self):
        return Empresa.objects.filter(cnae=self.cnae)

    
    # Helpers de Django
    # ------------------------------------------------------------------

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
