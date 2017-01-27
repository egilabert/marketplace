#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import numpy as np
import pandas as pd
from django.conf import settings
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
# Model Rating
# Tabla y funciones del model Empresa
# ------------------------------------------------------------------

class Rating(models.Model):

    # --- Variables de modelo ---
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    antiguedad = models.CharField(max_length=255)
    fondos_propios = models.BigIntegerField()
    activo_corriente = models.BigIntegerField()
    activo_no_corriente = models.BigIntegerField()
    pasivo_corriente = models.BigIntegerField()
    pasivo_no_corriente = models.BigIntegerField()
    importe_neto_cifra_negocio = models.BigIntegerField()
    gastos_financieros = models.BigIntegerField()
    resultados_antes_impuestos = models.BigIntegerField()

    # --- Parametros del modelo ---
    link = settings.DATA_FOLDER+'sectorial.csv'
    sectorial_data = pd.read_csv(link, encoding='latin1', sep=';', decimal=',')
    link = settings.DATA_FOLDER+'sectores.csv'
    sectores_data = pd.read_csv(link, encoding='latin1', sep=';', decimal=',')
    m_activo_corriente = [1.010126, 0.6905959, 0.3511273, 0]
    m_ratio_autonomia_financiera = [0, 0.1646282, 0.6776536, 1.29607]
    m_gastos_financiera_entre_ventas = [0.9693287, 0.8044454, 0.3827373, 0]
    m_resultados_entre_ventas = [0, 0.2427986, 0.3750541, 0.6537845]
    m_grupo_sectorial = [0, 0.05615981, 0.4273994, 1.064419]
    m_independiente = -0.2205067
    tramos = None
    rating = None
    tramos_grafico = None

    # Seleccionar de la tabla de valores medios sectoriales los valores del sector
    def get_sector_params(self, sector):
        return self.sectores_data[self.sectores_data['SECTOR'] == sector]

    # Traducir mediante los percentiles el tramo en el que nos encontramos
    def get_tramo(self, input_data, data, var):
        tramo = 0
        for index, row in data.iterrows():
            tramo += 1
            if row[var]>input_data:
                return tramo
        return 4

    # Seleccionar el tramo como traducción del sector de actividad
    def tramo_grupo_sectorial(self):
        if self.get_sector_params(self.sector)['AGRUPACI_N'].values=="MUY BUENO":
            return 4
        elif self.get_sector_params(self.sector)['AGRUPACI_N'].values=="BUENO":
            return 3
        elif self.get_sector_params(self.sector)['AGRUPACI_N'].values=="REGULAR":
            return 2
        elif self.get_sector_params(self.sector)['AGRUPACI_N'].values=="MALO":
            return 1
        else:
            return "error"

    # Traducción del rating en palabras para dar diagnóstico final
    def traduccion_rating(self, rating):
        if self.importe_neto_cifra_negocio<=900000:
            if rating<1.1:
                return "SITUACIÓN SECTORIAL MEJORABLE"
            elif rating<2.58:
                return "SITUACIÓN SECTORIAL BUENA"
            else:
                return "SITUACIÓN SECTORIAL EXCELENTE"
        else:
            if rating<0.96:
                return "SITUACIÓN SECTORIAL MEJORABLE"
            elif rating<2.58:
                return "SITUACIÓN SECTORIAL BUENA"
            else:
                return "SITUACIÓN SECTORIAL EXCELENTE"

    # Motor de cálculo del rating
    def rate_it(self):
        # Selección de datos sectoriales
        datos_sectorial = self.sectorial_data[self.sectorial_data['COD_SEC20'].isin(self.get_sector_params(self.sector)['#'].values)]
        # Cálculo de los tramos del modelo
        tramo_activo_corriente = self.get_tramo(self.activo_corriente, datos_sectorial, 'Activo_Corriente')
        tramo_r_Autonomia_Financiera = self.get_tramo(float(self.fondos_propios) / float(self.pasivo_corriente + self.pasivo_no_corriente + self.fondos_propios), datos_sectorial, 'R_Autonomia_Financiera')
        tramo_gastos_fin_entre_ventas = self.get_tramo(float(self.gastos_financieros)/float(self.importe_neto_cifra_negocio), datos_sectorial, 'R_Gastos_Financieros')
        tramo_resultados_entre_ventas = self.get_tramo(float(self.resultados_antes_impuestos)/float(self.importe_neto_cifra_negocio), datos_sectorial, 'R_Resultados_Sobre_Ventas')
        tramo_grupo_sectorial = self.tramo_grupo_sectorial()
        self.tramos = [tramo_activo_corriente, tramo_r_Autonomia_Financiera, tramo_gastos_fin_entre_ventas, tramo_resultados_entre_ventas, tramo_grupo_sectorial]


        self.tramos_grafico = [tramo_r_Autonomia_Financiera, tramo_gastos_fin_entre_ventas, tramo_resultados_entre_ventas, tramo_grupo_sectorial]
        
        self.rating = self.m_activo_corriente[tramo_activo_corriente-1] + self.m_ratio_autonomia_financiera[tramo_r_Autonomia_Financiera-1] + self.m_gastos_financiera_entre_ventas[tramo_gastos_fin_entre_ventas-1] + self.m_resultados_entre_ventas[tramo_resultados_entre_ventas-1] + self.m_grupo_sectorial[tramo_grupo_sectorial-1] + self.m_independiente
        return [self.rating, self.traduccion_rating(self.rating)]

    def ratio_solvencia(self):
        if (self.pasivo_corriente + self.pasivo_no_corriente) > 0:
            return float(self.activo_corriente) / float(self.pasivo_corriente + self.pasivo_no_corriente)
        else:
            return 0

    def ratio_endeudamiento(self):
        if (self.fondos_propios) > 0:
            return float(self.pasivo_corriente + self.pasivo_no_corriente) / float(self.fondos_propios)
        else:
            return 0

    def ratio_endeudamiento_cp(self):
        if (self.fondos_propios) > 0:
            return float(self.pasivo_corriente) / float(self.fondos_propios)
        else:
            return 0

    def ratio_autonomia(self):
        if (self.pasivo_corriente + self.pasivo_no_corriente) > 0:
            return float(self.fondos_propios) / float(self.pasivo_corriente + self.pasivo_no_corriente)
        else:
            return 0

    def ratio_cobertura_inmovilizado_FFPP(self):
        if (self.activo_no_corriente) > 0:
            return float(self.fondos_propios) / float(self.activo_no_corriente)
        else:
            return 0

    def ratio_rentabilidad_economica(self):
        if (self.activo_corriente + self.activo_no_corriente) > 0:
            return float(self.resultados_antes_impuestos) / float(self.activo_corriente + self.activo_no_corriente)
        else:
            return 0

    def ratio_autonomia_financiera(self):
        if (self.pasivo_corriente + self.pasivo_no_corriente + self.fondos_propios) > 0:
            return float(self.fondos_propios) / float(self.pasivo_corriente + self.pasivo_no_corriente + self.fondos_propios)
        else:
            return 0

    def ratio_dependencia_financiera(self):
        if (self.pasivo_corriente + self.pasivo_no_corriente + self.fondos_propios) > 0:
            return 1 - (float(self.fondos_propios) / float(self.pasivo_corriente + self.pasivo_no_corriente + self.fondos_propios))
        else:
            return 0

    def ratio_gastos_financieros(self):
        if (self.importe_neto_cifra_negocio) > 0:
            return float(self.gastos_financieros) / float(self.importe_neto_cifra_negocio)
        else:
            return 0

    def ratio_rentabilidad_financiera(self):
        if (self.fondos_propios) > 0:
            return float(self.resultados_antes_impuestos) / float(self.fondos_propios)
        else:
            return 0

    def ratio_rentabilidad_inversion(self):
        if (self.pasivo_corriente + self.pasivo_no_corriente) > 0:
            return float(self.resultados_antes_impuestos) / float(self.pasivo_corriente + self.pasivo_no_corriente)
        else:
            return 0

    def ratio_resultados_sobre_ventas(self):
        if (self.importe_neto_cifra_negocio) > 0:
            return float(self.resultados_antes_impuestos) / float(self.importe_neto_cifra_negocio)
        else:
            return 0

    def __unicode__(self):
        return self.name