#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import numpy as np
from django.db import models
from  django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Avg, Max, Min, Count, Sum, F
from django.db.models.functions import TruncMonth
from django.db.models import Prefetch
from calendar import monthrange
from datetime import datetime, timedelta
from django.utils.timezone import utc
import random

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

    temp_get_total_sells = None
    temp_get_sector_companies = None
    temp_get_clients = None 
    temp_get_total_sector_sells = None
    temp_margen_comercial_clientes = None
    temp_balance_clients_ebitda = None
    temp_balance_clients_payments = None
    temp_hhi_clients_sector_clients = None
    temp_hhi_geografical_clients = None
    temp_hhi_cnae_clients = None
    temp_hhi_temporal_clients = None
    temp_hhi_temporal_sector_clients = None
    temp_margen_comercial_sector_clientes = None
    temp_average_sector_sells = None
    temp_hhi_geografical_sector_clients = None
    temp_hhi_clients_clients = None
    temp_hhi_cnae_sector_clients = None
    temp_average_transfer_from_client = None
    temp_balance_providers_ebitda_avg_sector = None
    temp_get_total_buys = None
    temp_balance_providers_ebitda = None
    temp_my_penetration_provider = None
    temp_balance_providers_sells = None
    temp_average_sector_buys = None
    temp_get_total_sector_buys = None
    temp_hhi_providers_sector = None
    temp_hhi_providers = None
    temp_hhi_geografical_providers = None
    temp_hhi_geografical_sector_providers = None
    temp_hhi_cnae_sector_providers = None
    temp_hhi_cnae_providers = None
    temp_hhi_temporal_sector_providers = None
    temp_hhi_temporal_providers = None
    temp_get_sector_clients = None
    temp_get_clients = None
    temp_get_sector_providers = None
    temp_get_providers = None
    temp_margen_comercial_providers = None
    temp_margen_comercial_sector_providers = None
    temp_average_transfer_to_provider = None
    temp_balance_clients_ebitda_avg_sector = None
    temp_deuda_total = None
    temp_deuda_total_sector = None
    temp_deuda_corto_sector = None
    temp_deuda_largo_sector = None
    temp_deuda_largo = None
    temp_deuda_corto = None
    temp_riesgo_impago_clientes_sector = None
    temp_riesgo_impago_clientes = None

    def respuesta_clientes_ventas_hint(self):
        balance_sells_deviation = float(self.balance_clients_sells()[len(self.balance_clients_sells())-1].get('c', 0)-self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1].get('c', 0))/float(self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1].get('c', 0))
        if balance_sells_deviation > 0.5:
            return "Sigue así! Si buscas ampliar tu base de proveedores utiliza nuestro motor de recomendaciones."
        elif balance_sells_deviation > 0.1:
            return "Muy bien! Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones."
        elif balance_sells_deviation > -0.1:
            return "Bien! Si te interesa, puedes encontrar proveedores de mayor tamaño utilizando nuestro motor de recomendaciones."
        elif balance_sells_deviation > -0.5:
            return "Atención! Trabajar con proveedores más pequeños te da mayor poder de negociación pero puede aumentar el riesgo para tu empresa. Has probado con proveedores más grandes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
        else:
            return "Alerta! Trabajar con proveedores muy pequeños da mayor poder de negociación pero puede aumentar el riesgo para tu empresa. Has probado con proveedores más grandes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones."

    def riesgo_impago_clientes(self):
        if self.temp_riesgo_impago_clientes is None:
            group_by = self.get_clients().values('hats_alert').annotate(c=Sum('transfers__amount'))
            total = 0
            for alert in group_by:
                total += alert.get('c', 0)
            joined = False
            found = False
            key = ''
            value = 0
            ri = []
            if total > 0:
                for alert in group_by:
                    alert['c'] = float(alert.get('c', 0))/float(total)
                    if (alert['hats_alert']=='SIN ALERTA' or alert['hats_alert']=='VERDE'):
                        if found==False:
                            value = alert.get('c', 0)
                            key = alert['hats_alert']
                            found = True
                        elif joined==False:
                            alert['c'] += value
                            alert['hats_alert'] = 'VERDE'
                            ri.append(alert)
                            joined = True
                    else:
                        ri.append(alert)
                self.temp_riesgo_impago_clientes = ri
            else:
                self.temp_riesgo_impago_clientes = 0
            return self.temp_riesgo_impago_clientes
        return self.temp_riesgo_impago_clientes

    def riesgo_impago_proveedores(self):
        if self.temp_riesgo_impago_clientes is None:
            group_by = self.get_providers().values('hats_alert').annotate(c=Sum('transfers__amount'))
            total = 0
            for alert in group_by:
                total += alert.get('c', 0)
            joined = False
            found = False
            key = ''
            value = 0
            ri = []
            if total > 0:
                for alert in group_by:
                    alert['c'] = float(alert.get('c', 0))/float(total)
                    if (alert['hats_alert']=='SIN ALERTA' or alert['hats_alert']=='VERDE'):
                        if found==False:
                            value = alert.get('c', 0)
                            key = alert['hats_alert']
                            found = True
                        elif joined==False:
                            alert['c'] += value
                            alert['hats_alert'] = 'VERDE'
                            ri.append(alert)
                            joined = True
                    else:
                        ri.append(alert)
                self.temp_riesgo_impago_clientes = ri
            else:
                self.temp_riesgo_impago_clientes = 0
            return self.temp_riesgo_impago_clientes
        return self.temp_riesgo_impago_clientes

    def riesgo_impago_clientes_sector(self):
        if self.temp_riesgo_impago_clientes_sector is None:
            group_by = self.clients_of_sector_companies().values('hats_alert').annotate(c=Sum('transfers__amount'))
            total = 0
            for alert in group_by:
                total += alert.get('c', 0)
            joined = False
            found = False
            key = ''
            value = 0
            ri = []
            if total > 0:
                for alert in group_by:
                    alert['c'] = float(alert.get('c', 0))/float(total)
                    if (alert['hats_alert']=='SIN ALERTA' or alert['hats_alert']=='VERDE'):
                        if found==False:
                            value = alert.get('c', 0)
                            key = alert['hats_alert']
                            found = True
                        elif joined==False:
                            alert['c'] += value
                            alert['hats_alert'] = 'VERDE'
                            ri.append(alert)
                            joined = True
                    else:
                        ri.append(alert)
                self.temp_riesgo_impago_clientes_sector = ri
            else:
                self.temp_riesgo_impago_clientes = 0
            return self.temp_riesgo_impago_clientes_sector
        return self.temp_riesgo_impago_clientes_sector

    def riesgo_impago_providers_sector(self):
        if self.temp_riesgo_impago_clientes_sector is None:
            group_by = self.providers_of_sector_companies().values('hats_alert').annotate(c=Sum('transfers__amount'))
            total = 0
            for alert in group_by:
                total += alert.get('c', 0)
            joined = False
            found = False
            key = ''
            value = 0
            ri = []
            if total > 0:
                for alert in group_by:
                    alert['c'] = float(alert.get('c', 0))/float(total)
                    if (alert['hats_alert']=='SIN ALERTA' or alert['hats_alert']=='VERDE'):
                        if found==False:
                            value = alert.get('c', 0)
                            key = alert['hats_alert']
                            found = True
                        elif joined==False:
                            alert['c'] += value
                            alert['hats_alert'] = 'VERDE'
                            ri.append(alert)
                            joined = True
                    else:
                        ri.append(alert)
                self.temp_riesgo_impago_clientes_sector = ri
            else:
                self.temp_riesgo_impago_clientes = 0
            return self.temp_riesgo_impago_clientes_sector
        return self.temp_riesgo_impago_clientes_sector

    def clients_of_sector_companies(self):
        if self.temp_get_sector_clients is None:
            self.temp_get_sector_clients = Empresa.objects.filter(transfers__destination_reference__in=self.get_sector_companies()).annotate(Count('name', distinct=True))
        return self.temp_get_sector_clients

    def providers_of_sector_companies(self):
        if self.temp_get_sector_providers is None:
            self.temp_get_sector_providers = Empresa.objects.filter(destination_reference__origin_reference__in=self.get_sector_companies()).annotate(Count('name', distinct=True))
        return self.temp_get_sector_providers

    def productos_con_tipo_variable(self):
        return Productos.objects.filter(empresa=self, desc_producto__icontains='var')

    def respuesta_sabia(self):
        if self.hhi_clients_clients() > -0.1:
            return "El Índice de Herfindahl es una medida, empleada en economía, que informa sobre la concentración económica de un mercado. O, inversamente, la medida de falta de competencia en un sistema económico. Un índice elevado expresa un mercado muy concentrado y poco competitivo (valores de 0 a 1)."
        else:
            return "hola"

    def my_penetration_client(self):
        if self.balance_clients_payments():
            if len(self.balance_clients_payments())>0 and self.balance_clients_payments()[len(self.balance_clients_payments())-1] > 0:
                return float(self.get_total_sells())/float(self.balance_clients_payments()[len(self.balance_clients_payments())-1])
        return 0

    def my_penetration_provider(self):
        if self.temp_my_penetration_provider is None:
            if self.balance_providers_sells() and list(self.balance_providers_sells())[len(list(self.balance_providers_sells()))-1].get('c', 0)>0:
                self.temp_my_penetration_provider = float(self.get_total_buys())/floatfloat(list(self.balance_providers_sells())[len(list(self.balance_providers_sells()))-1].get('c', 0))
                return self.temp_my_penetration_provider
            self.temp_my_penetration_provider = 0
            return self.temp_my_penetration_provider
        return self.temp_my_penetration_provider

    def my_sector_penetration_client(self):
        if len(self.balance_clients_payments_avg_sector())>0 and self.balance_clients_payments_avg_sector()[len(self.balance_clients_payments_avg_sector())-1]>0:
            return float(self.get_total_sector_sells())/float(self.balance_clients_payments_avg_sector()[len(self.balance_clients_payments_avg_sector())-1])
        return 0

    def hhi_providers(self):
        if self.temp_hhi_providers is None:
            groub_by = self.get_providers().values('name').annotate(c=Sum('destination_reference__amount'))
            total = self.get_total_buys()
            hhi = 0
            if total > 0:
                for i, name in enumerate(groub_by):
                    one = float(name.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_providers = hhi
            else:
                self.temp_hhi_providers = 0
        return self.temp_hhi_providers

    def hhi_providers_sector(self):
        if self.temp_hhi_providers_sector is None:
            groub_by = self.providers_of_sector_companies().values('name').annotate(c=Sum('destination_reference__amount'))
            total = self.get_total_sector_buys()
            hhi = 0
            total_by = 0
            if total>0:
                for i, name in enumerate(groub_by):
                    one = float(name.get('c', 0))
                    total_by += one
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_providers_sector = hhi
            else:
                self.temp_hhi_providers_sector = 0
        return self.temp_hhi_providers_sector

    def hhi_clients_clients(self):
        if self.temp_hhi_clients_clients is None:
            groub_by = self.get_clients().values('name').annotate(c=Sum('transfers__amount'))
            total = self.get_total_sells()
            hhi = 0
            if total > 0:
                for i, name in enumerate(groub_by):
                    one = float(name.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_clients_clients = hhi
            else:
                self.temp_hhi_clients_clients = 0
        return self.temp_hhi_clients_clients

    def hhi_clients_sector_clients(self):
        if self.temp_hhi_clients_sector_clients is None:
            groub_by = self.clients_of_sector_companies().values('name').annotate(c=Sum('transfers__amount'))
            total = self.get_total_sector_sells()
            hhi = 0
            if total > 0:
                for i, name in enumerate(groub_by):
                    one = float(name.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_clients_sector_clients = hhi
            else:
                self.temp_hhi_clients_sector_clients = 0
        return self.temp_hhi_clients_sector_clients

    def hhi_geografical_clients(self):
        if self.temp_hhi_geografical_clients is None:
            groub_by = self.get_clients().values('territorial').annotate(c=Sum('transfers__amount'))
            total = self.get_total_sells()
            hhi = 0
            if total > 0:
                for i, territorial in enumerate(groub_by):
                    one = float(territorial.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_geografical_clients = hhi
            else:
                self.temp_hhi_geografical_clients = 0
        return self.temp_hhi_geografical_clients

    def hhi_geografical_sector_clients(self):
        if self.temp_hhi_geografical_sector_clients is None:
            groub_by = self.clients_of_sector_companies().values('territorial').annotate(c=Sum('transfers__amount'))
            total = self.get_total_sector_sells()
            hhi = 0
            if total>0:
                for i, territorial in enumerate(groub_by):
                    one = float(territorial.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_geografical_sector_clients = hhi
            else:
                self.temp_hhi_geografical_sector_clients = 0
        return self.temp_hhi_geografical_sector_clients

    def hhi_geografical_providers(self):
        if self.temp_hhi_geografical_providers is None:
            groub_by = self.get_providers().values('territorial').annotate(c=Sum('destination_reference__amount'))
            total = self.get_total_buys()
            hhi = 0
            if total > 0:
                for i, territorial in enumerate(groub_by):
                    one = float(territorial.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_geografical_providers = hhi
            else:
                self.temp_hhi_geografical_providers = 0
        return self.temp_hhi_geografical_providers

    def hhi_geografical_sector_providers(self):
        if self.temp_hhi_geografical_sector_providers is None:
            groub_by = self.providers_of_sector_companies().values('territorial').annotate(c=Sum('destination_reference__amount'))
            total = self.get_total_sector_buys()
            hhi = 0
            if total > 0:
                for i, territorial in enumerate(groub_by):
                    one = float(territorial.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_geografical_sector_providers = hhi
            else:
                self.temp_hhi_geografical_sector_providers = 0
        return self.temp_hhi_geografical_sector_providers

    def hhi_cnae_clients(self):
        if self.temp_hhi_cnae_clients is None:
            groub_by = self.get_clients().values('cnae').annotate(c=Sum('transfers__amount'))
            total = self.get_total_sells()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_cnae_clients = hhi
            else:
                self.temp_hhi_cnae_clients = 0
        return self.temp_hhi_cnae_clients

    def hhi_cnae_sector_clients(self):
        if self.temp_hhi_cnae_sector_clients is None:
            groub_by = self.clients_of_sector_companies().values('cnae').annotate(c=Sum('transfers__amount'))
            total = self.get_total_sector_sells()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_cnae_sector_clients = hhi
            else:
                self.temp_hhi_cnae_sector_clients = 0
        return self.temp_hhi_cnae_sector_clients

    def hhi_cnae_providers(self):
        if self.temp_hhi_cnae_providers is None:
            groub_by = self.get_providers().values('cnae').annotate(c=Sum('destination_reference__amount'))
            total = self.get_total_buys()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_cnae_providers = hhi
            else:
                self.temp_hhi_cnae_providers = 0
        return self.temp_hhi_cnae_providers

    def hhi_cnae_sector_providers(self):
        if self.temp_hhi_cnae_sector_providers is None:
            groub_by = self.providers_of_sector_companies().values('cnae').annotate(c=Sum('destination_reference__amount'))
            total = self.get_total_sector_buys()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_cnae_sector_providers = hhi
            else:
                self.temp_hhi_cnae_sector_providers = 0
        return self.temp_hhi_cnae_sector_providers

    def hhi_temporal_clients(self):
        if self.temp_hhi_temporal_clients is None:
            groub_by = self.get_monthly_sells_amount()
            total = self.get_total_sells()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_temporal_clients = hhi
            else:
                self.temp_hhi_temporal_clients = 0
        return self.temp_hhi_temporal_clients

    def hhi_temporal_sector_clients(self):
        if self.temp_hhi_temporal_sector_clients is None:
            groub_by = self.get_sector_total_monthly_sells_amount()
            total = self.get_total_sector_sells()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_temporal_sector_clients = hhi
            else:
                self.temp_hhi_temporal_sector_clients = 0
        return self.temp_hhi_temporal_sector_clients

    def hhi_temporal_providers(self):
        if self.temp_hhi_temporal_providers is None:
            groub_by = self.get_monthly_buys_amount()
            total = self.get_total_buys()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_temporal_providers = hhi
            else:
                self.temp_hhi_temporal_providers = 0
        return self.temp_hhi_temporal_providers

    def hhi_temporal_sector_providers(self):
        if self.temp_hhi_temporal_sector_providers is None:
            groub_by = self.get_sector_total_monthly_buys_amount()
            total = self.get_total_sector_buys()
            hhi = 0
            if total > 0:
                for i, cnae in enumerate(groub_by):
                    one = float(cnae.get('c', 0))
                    total = float(total)
                    hhi += pow(one/total,2)
                self.temp_hhi_temporal_sector_providers = hhi
            else:
                self.temp_hhi_temporal_sector_providers = 0
        return self.temp_hhi_temporal_sector_providers

    # Helpers de los estados financieros
    # ------------------------------------------------------------------

    def margen_comercial_clientes(self):
        if self.temp_margen_comercial_clientes is None:
            ebitda = self.balance_clients_ebitda().last()
            ventas = self.balance_clients_sells().last()
            if (ebitda is None) or (ventas is None):
                self.temp_margen_comercial_clientes = 0
                return self.temp_margen_comercial_clientes
            elif (float(ventas.get('c', 0)-ebitda.get('c', 0))==0):
                self.temp_margen_comercial_clientes = 0
                return self.temp_margen_comercial_clientes
            self.temp_margen_comercial_clientes = float(ebitda.get('c', 0))/float(ventas.get('c', 0)-ebitda.get('c', 0))
        return self.temp_margen_comercial_clientes

    def margen_comercial_sector_clientes(self):
        if self.temp_margen_comercial_sector_clientes is None:
            ebitda = self.balance_clients_ebitda_avg_sector().last()
            ventas = self.balance_clients_sells_avg_sector().last()
            if (ebitda is None) or (ventas is None):
                self.temp_margen_comercial_sector_clientes = 0
                return self.temp_margen_comercial_sector_clientes
            elif float(ventas.get('c', 0)-ebitda.get('c', 0))==0:
                self.temp_margen_comercial_sector_clientes = 0
                return self.temp_margen_comercial_sector_clientes
            self.temp_margen_comercial_sector_clientes = float(ebitda.get('c', 0))/float(ventas.get('c', 0)-ebitda.get('c', 0))
        return self.temp_margen_comercial_sector_clientes

    def margen_comercial_providers(self):
        if self.temp_margen_comercial_providers is None:
            if self.balance_providers_ebitda() and self.balance_providers_sells():
                ebitda = self.balance_providers_ebitda().last().get('c', 0)
                ventas = self.balance_providers_sells().last().get('c', 0)
                if float(ventas-ebitda)==0:
                    self.temp_margen_comercial_providers = 0
                    return self.temp_margen_comercial_providers
                self.temp_margen_comercial_providers = float(ebitda)/float(ventas-ebitda)
                return self.temp_margen_comercial_providers
            self.temp_margen_comercial_providers = 0
            return self.temp_margen_comercial_providers
        return self.temp_margen_comercial_providers

    def margen_comercial_sector_providers(self):
        if self.temp_margen_comercial_sector_providers is None:
            if self.balance_providers_ebitda_avg_sector() and self.balance_providers_sells_avg_sector():
                ebitda = self.balance_providers_ebitda_avg_sector().last().get('c', 0)
                ventas = self.balance_providers_sells_avg_sector().last().get('c', 0)
                if float(ventas-ebitda)==0:
                    self.temp_margen_comercial_sector_providers = 0
                    return self.temp_margen_comercial_sector_providers
                self.temp_margen_comercial_sector_providers = float(ebitda)/float(ventas-ebitda)
                return self.temp_margen_comercial_sector_providers
            return self.temp_margen_comercial_sector_providers
        return self.temp_margen_comercial_sector_providers

    def ratio_comercial_providers(self):
        return 1-self.margen_comercial_providers()

    def ratio_comercial_sector_providers(self):
        return 1-self.margen_comercial_sector_providers()

    def ratio_comercial_clientes(self):
        return 1-self.margen_comercial_clientes()

    def ratio_comercial_sector_clientes(self):
        return 1-self.margen_comercial_sector_clientes()

    def annual_balance_exercises(self):
        return self.estados_financieros.all().values('ejercicio').order_by('ejercicio')

    def annual_sector_balance_exercises(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).values('ejercicio').distinct().order_by('ejercicio')

    def resultado_explotacion(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('resultado_explotacion')).order_by('ejercicio')

    def resultado_explotacion_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(resultado_explotacion=0).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_clients_resultado(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_clients()).exclude(resultado_explotacion=0).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_clients_resultado_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.clients_of_sector_companies()).exclude(resultado_explotacion=0).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_providers_resultado(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_providers()).exclude(resultado_explotacion=0).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_providers_resultado_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.providers_of_sector_companies()).exclude(resultado_explotacion=0).values('ejercicio').annotate(c=Avg('resultado_explotacion')).order_by('ejercicio')

    def balance_clients_sells(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_clients()).exclude(ventas=0).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')

    def balance_clients_sells_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.clients_of_sector_companies()).exclude(ventas=0).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')

    def balance_providers_sells(self):
        if self.temp_balance_providers_sells is None:
            self.temp_balance_providers_sells = EstadosFinancieros.objects.filter(empresa__in=self.get_providers()).exclude(ventas=0).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')
        return self.temp_balance_providers_sells

    def balance_providers_sells_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.providers_of_sector_companies()).exclude(ventas=0).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')

    def balance_providers_buys(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_clients()).exclude(ventas=0).values('ejercicio').annotate(c=Avg(F('ventas')-F('ebitda'))).order_by('ejercicio')

    def balance_providers_buys_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.clients_of_sector_companies()).exclude(ventas=0).values('ejercicio').annotate(c=Avg(F('ventas')-F('ebitda'))).order_by('ejercicio')

    def balance_sells(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('ventas')).order_by('ejercicio')

    def balance_sells_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(ventas=0).values('ejercicio').annotate(c=Avg('ventas')).order_by('ejercicio')

    def balance_buys(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum(F('ventas')-F('ebitda'))).order_by('ejercicio')

    def balance_buys_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(ventas=0).values('ejercicio').annotate(c=Avg(F('ventas')-F('ebitda'))).order_by('ejercicio')

    def balance_depreciation(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('depreciaciones')).order_by('ejercicio')

    def balance_depreciation_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(depreciaciones=0).values('ejercicio').annotate(c=Avg('depreciaciones')).order_by('ejercicio')

    def balance_amortisation(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('amortizaciones')).order_by('ejercicio')

    def balance_amortisation_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(amortizaciones=0).values('ejercicio').annotate(c=Avg('amortizaciones')).order_by('ejercicio')

    def balance_clients_payments(self):
        if self.temp_balance_clients_payments is None:
            ebitda = self.balance_clients_ebitda()
            earnings = self.balance_clients_sells()
            payments = []
            for i, ejercicio in enumerate(ebitda):
                if len(earnings)>=i+1:
                    payments.append(earnings[i].get('c', 0)-ebitda[i].get('c', 0))
            self.temp_balance_clients_payments = payments
        return self.temp_balance_clients_payments

    def balance_clients_payments_avg_sector(self):
        ebitda = self.balance_clients_ebitda_avg_sector()
        earnings = self.balance_clients_sells_avg_sector()
        payments = []
        for i, ejercicio in enumerate(ebitda):
            payments.append(earnings[i].get('c', 0)-ebitda[i].get('c', 0))
        return payments

    def balance_ebitda(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('ebitda')).order_by('ejercicio')

    def balance_ebitda_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(ebitda=0).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')
    
    def balance_clients_ebitda(self):
        if self.temp_balance_clients_ebitda is None:
            self.temp_balance_clients_ebitda = EstadosFinancieros.objects.filter(empresa__in=self.get_clients()).exclude(ebitda=0).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')
        return self.temp_balance_clients_ebitda

    def balance_clients_ebitda_avg_sector(self):
        if self.temp_balance_clients_ebitda_avg_sector is None:
            self.temp_balance_clients_ebitda_avg_sector = EstadosFinancieros.objects.filter(empresa__in=self.clients_of_sector_companies()).exclude(ebitda=0).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')
        return self.temp_balance_clients_ebitda_avg_sector

    def balance_providers_ebitda(self):
        if self.temp_balance_providers_ebitda is None:
            self.temp_balance_providers_ebitda = EstadosFinancieros.objects.filter(empresa__in=self.get_providers()).exclude(ebitda=0).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')
        return self.temp_balance_providers_ebitda

    def balance_providers_ebitda_avg_sector(self):
        if self.temp_balance_providers_ebitda_avg_sector is None:
            self.temp_balance_providers_ebitda_avg_sector = EstadosFinancieros.objects.filter(empresa__in=self.providers_of_sector_companies()).exclude(ebitda=0).values('ejercicio').annotate(c=Avg('ebitda')).order_by('ejercicio')
        return self.temp_balance_providers_ebitda_avg_sector

    def balance_stock(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('existencias')).order_by('ejercicio')

    def balance_stock_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(existencias=0).values('ejercicio').annotate(c=Avg('existencias')).order_by('ejercicio')

    def balance_deudores(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('deudores')).order_by('ejercicio')

    def balance_deudores_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(deudores=0).values('ejercicio').annotate(c=Avg('deudores')).order_by('ejercicio')

    def balance_acreedores_comerciales(self):
        return self.estados_financieros.all().values('ejercicio').annotate(c=Sum('acreedores_comerciales')).order_by('ejercicio')

    def balance_acreedores_comerciales_avg_sector(self):
        return EstadosFinancieros.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(acreedores_comerciales=0).values('ejercicio').annotate(c=Avg('acreedores_comerciales')).order_by('ejercicio')

    # Helpers de transferencias
    # ------------------------------------------------------------------

    def average_transfer_to_provider(self):
        if self.temp_average_transfer_to_provider is None:
            group_by = self.transfers.all().exclude(amount=0).aggregate(avg=Avg('amount'))
            self.temp_average_transfer_to_provider = group_by['avg']
            return self.temp_average_transfer_to_provider
        return self.temp_average_transfer_to_provider

    def average_transfer_from_client(self):
        if self.temp_average_transfer_from_client is None:
            group_by = self.destination_reference.all().exclude(amount=0).aggregate(avg=Avg('amount'))
            self.temp_average_transfer_from_client = group_by['avg']
        return self.temp_average_transfer_from_client

    def get_clients(self):
        if self.temp_get_clients is None:
            self.temp_get_clients = Empresa.objects.filter(transfers__destination_reference=self).annotate(Count('name', distinct=True))
        return self.temp_get_clients

    def get_providers(self):
        if self.temp_get_providers is None:
            self.temp_get_providers = Empresa.objects.filter(destination_reference__in=Transfer.objects.filter(origin_reference=self)).annotate(Count('name', distinct=True))
        return self.temp_get_providers

    def get_monthly_buys(self):
        group_by = self.transfers.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('month')
        for month in group_by:
            month['month'] = month['month'].strftime("%b %Y")
        return group_by

    def get_monthly_sells(self):
        group_by = self.destination_reference.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('month')
        for month in group_by:
            month['month'] = month.get('month', None).strftime("%b %Y") 
        return group_by

    def get_monthly_sector_avg_sells(self):
        group_by = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Count('id')).order_by('month')
        for month in group_by:
            if self.get_sector_companies().count()>0:
                month['c'] = month.get('c', 0)/self.get_sector_companies().count()
            else:
                month['c'] = 0
            month['month'] = month.get('month', None).strftime("%b %Y")
        return group_by

    def get_monthly_buys_amount(self):
        group_by = self.transfers.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('month')
        for month in group_by:
            month['month'] = month.get('month', None).strftime("%b %Y") 
        return group_by

    def get_monthly_sells_amount(self):
        group_by = self.destination_reference.all().annotate(month=TruncMonth('operation_data')).values('month').annotate(c=Sum('amount')).order_by('month')
        for month in group_by:
            month['month'] = month.get('month', None).strftime("%b %Y") 
        return group_by

    def get_total_buys(self):
        if self.temp_get_total_buys is None:
            total = self.transfers.all().aggregate(total=Sum('amount'))
            self.temp_get_total_buys = total['total']
        return self.temp_get_total_buys

    def get_total_sells(self):
        if self.temp_get_total_sells is None: 
            total = self.destination_reference.all().aggregate(total=Sum('amount'))
            self.temp_get_total_sells = total['total']
        return self.temp_get_total_sells

    def get_total_sector_buys(self):
        if self.temp_get_total_sector_buys is None:
            total = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).aggregate(total=Sum('amount'))
            self.temp_get_total_sector_buys = total['total']
        return self.temp_get_total_sector_buys

    def average_sector_buys(self):
        if self.temp_average_sector_buys is None:
            total = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).exclude(amount=0).aggregate(total=Avg('amount'))
            self.temp_average_sector_buys = total['total']
        return self.temp_average_sector_buys

    def get_total_sector_sells(self):
        if self.temp_get_total_sector_sells is None:
            print('Calculating temp_get_total_sector_sells...')
            self.temp_get_total_sector_sells = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).aggregate(total=Sum('amount'))
        return self.temp_get_total_sector_sells['total']

    def average_sector_sells(self):
        if self.temp_average_sector_sells is None:
            total = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).exclude(amount=0).aggregate(total=Avg('amount'))
            self.temp_average_sector_sells = total['total']
        return self.temp_average_sector_sells

    def get_sector_avg_monthly_sells_amount(self):
        group_by = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).exclude(amount=0).values('month').annotate(c=Avg('amount')).order_by('month')
        return group_by

    def get_sector_avg_monthly_buys_amount(self):
        group_by = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).exclude(amount=0).values('month').annotate(c=Avg('amount')).order_by('month')
        return group_by

    def get_sector_total_monthly_sells_amount(self):
        group_by = Transfer.objects.filter(destination_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).exclude(amount=0).values('month').annotate(c=Sum('amount')).order_by('month')
        for month in group_by:
            month['month'] = month.get('month', None).strftime("%b %Y") 
        return group_by

    def get_sector_total_monthly_buys_amount(self):
        group_by = Transfer.objects.filter(origin_reference__in=self.get_sector_companies().all()).annotate(month=TruncMonth('operation_data')).exclude(amount=0).values('month').annotate(c=Sum('amount')).order_by('month')
        return group_by

    def get_qs_clients(self,qs):
        return Empresa.objects.filter(transfers__destination_reference__in=qs).annotate(Count('name', distinct=True))

    def get_qs_providers(self,qs):
        return Empresa.objects.filter(destination_reference__in=Transfer.objects.filter(origin_reference__in=qs)).annotate(Count('name', distinct=True))

    def clients_by_region(self):
        return Empresa.objects.filter(transfers__destination_reference=self).all().values('territorial').annotate(c=Sum('transfers__amount'))

    def providers_by_region(self):
        return Empresa.objects.filter(destination_reference__origin_reference=self).all().values('territorial').annotate(c=Sum('transfers__amount'))

    def clients_by_sector(self):
        return Empresa.objects.filter(transfers__destination_reference=self).all().values('cnae').annotate(c=Sum('transfers__amount'))

    def providers_by_sector(self):
        return Empresa.objects.filter(destination_reference__origin_reference=self).all().values('cnae').annotate(c=Sum('transfers__amount'))
    
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
        if self.temp_get_sector_companies is None:
            self.temp_get_sector_companies = Empresa.objects.filter(cnae=self.cnae).exclude(fiscal_id=self.fiscal_id)
        return self.temp_get_sector_companies

    # Helpers de CIRBE
    # ------------------------------------------------------------------

    def deuda_total(self):
        if self.temp_deuda_total is None:
            self.temp_deuda_total = self.cirbe.largo_plazo_dispuesto + self.cirbe.corto_plazo_dispuesto
        return self.temp_deuda_total

    def deuda_total_sector(self):
        if self.temp_deuda_total_sector is None:
            self.temp_deuda_corto_sector = CIRBE.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(corto_plazo_dispuesto=0).aggregate(c=Avg('corto_plazo_dispuesto'))
            self.temp_deuda_largo_sector = CIRBE.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(largo_plazo_dispuesto=0).aggregate(c=Avg('largo_plazo_dispuesto'))
            self.temp_deuda_total_sector = self.temp_deuda_corto_sector.get('c', 0) + self.temp_deuda_largo_sector.get('c', 0)
        return self.temp_deuda_total_sector

    def deuda_corto(self):
        if self.temp_deuda_corto is None:
            self.temp_deuda_corto = self.cirbe.corto_plazo_dispuesto
        return self.temp_deuda_corto

    def deuda_corto_sector(self):
        if self.temp_deuda_corto_sector is None:
            self.temp_deuda_corto_sector = CIRBE.objects.filter(empresa__in=self.get_sector_companies().all()).aggregate(c=Avg('corto_plazo_dispuesto'))
        return self.temp_deuda_corto_sector.get('c', 0)

    def deuda_corto_pond(self):
        if len(self.balance_ebitda()) > 0:
            if self.balance_ebitda()[len(self.balance_ebitda())-1].get('c', 0)>0:
                return self.deuda_corto()/float(self.balance_ebitda()[len(self.balance_ebitda())-1].get('c', 0))
            return 04
        return 0

    def deuda_corto_sector_pond(self):
        if len(self.balance_ebitda_avg_sector()) > 0:
            if self.balance_ebitda_avg_sector()[len(self.balance_ebitda_avg_sector())-1].get('c', 0)>0:
                return float(self.deuda_corto_sector())/float(self.balance_ebitda_avg_sector()[len(self.balance_ebitda_avg_sector())-1].get('c', 0))
            return 0
        return 0

    def deuda_largo(self):
        if self.temp_deuda_largo is None:
            self.temp_deuda_largo = self.cirbe.largo_plazo_dispuesto
        return self.temp_deuda_largo

    def deuda_largo_sector(self):
        if self.temp_deuda_largo_sector is None:
            self.temp_deuda_largo_sector = CIRBE.objects.filter(empresa__in=self.get_sector_companies().all()).exclude(largo_plazo_dispuesto=0).aggregate(c=Avg('largo_plazo_dispuesto'))
            if self.temp_deuda_largo_sector:
                return self.temp_deuda_largo_sector.get('c', 0)
            else:
                return 0
        return self.temp_deuda_largo_sector.get('c', 0)

    def deuda_largo_pond(self):
        if len(self.balance_sells()) > 0 and float(self.balance_sells()[len(self.balance_sells())-1].get('c', 0)) > 0:
            return self.deuda_largo()/float(self.balance_sells()[len(self.balance_sells())-1].get('c', 0))
        return 0

    def deuda_largo_sector_pond(self):
        if len(self.balance_sells_avg_sector()) > 0 and float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0)) > 0:
            return float(self.deuda_largo_sector())/float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0))
        return 0

    def deuda_total_pond(self):
        if len(self.balance_sells()) > 0 and float(self.balance_sells()[len(self.balance_sells())-1].get('c', 0)) > 0:
            return (self.deuda_largo()+self.deuda_corto())/float(self.balance_sells()[len(self.balance_sells())-1].get('c', 0))
        return 0

    def deuda_total_sector_pond(self):
        if len(self.balance_sells_avg_sector()) > 0 and float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0)) > 0:
            return float(self.deuda_largo_sector()+self.deuda_corto())/float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0))
        return 0

    def gastos_financiero(self):
        if self.deuda_total():
            return self.deuda_total()*random.uniform(0.03, 0.06)
        return 0

    def gastos_financiero_sector(self):
        if self.deuda_total_sector():
            return self.deuda_total_sector()*random.uniform(0.04, 0.05)
        return 0

    def costes_financiacion(self):
        if self.deuda_total() and self.deuda_total() > 0:
            return self.gastos_financiero()/self.deuda_total()
        return 0

    def costes_financiacion_sector(self):
        if self.deuda_total_sector() and self.deuda_total_sector()>0:
            return self.gastos_financiero_sector()/self.deuda_total_sector()
        return 0

    def deuda_largo_sector_pond(self):
        if len(self.balance_sells_avg_sector()) > 0 and float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0)) > 0:
            return float(self.deuda_largo_sector())/float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0))
        return 0

    def ratio_corto_largo(self):
        if self.deuda_largo() > 0:
            return float(self.deuda_corto()) / float(self.deuda_largo())
        return 0

    def ratio_sector_corto_largo(self):
        if self.deuda_largo_sector() > 0:
            return self.deuda_corto_sector() / self.deuda_largo_sector()
        return 0

    def dias_a_cobrar(self):
        if len(self.balance_sells()) > 0 and self.balance_deudores():
            if self.balance_sells()[len(self.balance_sells())-1].get('c', 0) > 0:
                return 365*(self.balance_deudores()[len(self.balance_deudores())-1].get('c', 0) / self.balance_sells()[len(self.balance_sells())-1].get('c', 0))
            return 0
        return 0

    def dias_a_cobrar_sector(self):
        if len(self.balance_sells_avg_sector()) > 0 and self.balance_deudores_avg_sector():
            if self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0) > 0:
                return 365*(self.balance_deudores_avg_sector()[len(self.balance_deudores_avg_sector())-1].get('c', 0) / self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1].get('c', 0))
            return 0
        return 0

    def dias_a_pagar(self):
        if len(self.balance_buys()) > 0 and self.balance_acreedores_comerciales():
            if self.balance_buys()[len(self.balance_buys())-1].get('c', 0) > 0:
                return 365*(self.balance_acreedores_comerciales()[len(self.balance_acreedores_comerciales())-1].get('c', 0) / self.balance_buys()[len(self.balance_buys())-1].get('c', 0))
            return 0
        return 0

    def dias_a_pagar_sector(self):
        if len(self.balance_buys_avg_sector()) > 0 and self.balance_acreedores_comerciales_avg_sector():
            if self.balance_buys_avg_sector()[len(self.balance_buys_avg_sector())-1].get('c', 0) > 0:
                return 365*(self.balance_acreedores_comerciales_avg_sector()[len(self.balance_acreedores_comerciales_avg_sector())-1].get('c', 0) / self.balance_buys_avg_sector()[len(self.balance_buys_avg_sector())-1].get('c', 0))
            return 0
        return 0

    def get_sector_clients(self):
        return self.clients_of_sector_companies().count()

    def get_sector_providers(self):
        return self.providers_of_sector_companies().count()

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

    class Meta:
        ordering = ['ejercicio']

# ------------------------------------------------------------------
# Model Productos
# Tabla y funciones del model Productos (contratados por una empresa)
# ------------------------------------------------------------------
class Productos(models.Model):

    empresa = models.ForeignKey(Empresa, related_name='productos', null=True, blank=True, on_delete=models.CASCADE)
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

    temp_plazo_total = None
    temp_plazo_remanente = None
    temp_cuota_mensual = None
    temp_cuota_mensual_mas_1 = None

    def plazo_total(self):
        if self.temp_plazo_total is None:
            if self.fecha_vencimiento and self.fecha_formalizacion:
                self.temp_plazo_total = self.monthdelta(self.fecha_formalizacion, self.fecha_vencimiento) + 1
            else:
                self.temp_plazo_total = 0
        return self.temp_plazo_total

    def plazo_remanente(self):
        if self.temp_plazo_remanente is None:
            if self.fecha_vencimiento:
                now = datetime.utcnow().replace(tzinfo=utc)
                self.temp_plazo_remanente = self.monthdelta(datetime.date(now), self.fecha_vencimiento) + 1
            else:
                self.temp_plazo_remanente = 0
        return self.temp_plazo_remanente

    def cuota_mensual(self):
        if self.temp_cuota_mensual is None:
            if self.interes_revisado and self.plazo_remanente and self.dispuesto:
                self.temp_cuota_mensual = np.pmt(self.interes_revisado/12, self.plazo_remanente(), -self.dispuesto)
            else:
                self.temp_cuota_mensual = 0
        return self.temp_cuota_mensual

    def cuota_mensual_mas_1(self):
        if self.temp_cuota_mensual_mas_1 is None:
            if self.interes_revisado and self.plazo_remanente and self.dispuesto:
                self.temp_cuota_mensual_mas_1 = np.pmt((self.interes_revisado+0.01)/12, self.plazo_remanente(), -self.dispuesto)
            else:
                self.temp_cuota_mensual_mas_1 = 0
        return self.temp_cuota_mensual_mas_1

    def monthdelta(self, d1, d2):
        delta = 0
        while True:
            mdays = monthrange(d1.year, d1.month)[1]
            d1 += timedelta(days=mdays)
            if d1 <= d2:
                delta += 1
            else:
                break
        return delta



    def __unicode__(self):
        return self.tipo_producto

# ------------------------------------------------------------------
# Model CIRBE
# Tabla y funciones del model CIRBE (contratados por una empresa)
# ------------------------------------------------------------------
class CIRBE(models.Model):

    empresa = models.OneToOneField(Empresa, related_name='cirbe', null=True, blank=True, on_delete=models.CASCADE)
    cirbe_concedido = models.IntegerField(null=True, blank=True)
    cirbe_dispuesto = models.IntegerField(null=True, blank=True)
    largo_plazo_concedido = models.IntegerField(null=True, blank=True)
    largo_plazo_dispuesto = models.IntegerField(null=True, blank=True)
    largo_plazo_concedido = models.IntegerField(null=True, blank=True)
    corto_plazo_dispuesto = models.IntegerField(null=True, blank=True)
    d_concedido = models.IntegerField(null=True, blank=True)
    d_dispuesto = models.IntegerField(null=True, blank=True)
    avales_concedido = models.IntegerField(null=True, blank=True)
    avales_dispuesto = models.IntegerField(null=True, blank=True)
    leasing_concedido = models.IntegerField(null=True, blank=True)
    leasing_dispuesto = models.IntegerField(null=True, blank=True)
    sr_concedido = models.IntegerField(null=True, blank=True)
    sr_dispuesto = models.IntegerField(null=True, blank=True)
    moroso = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return str(self.cirbe_concedido)

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
