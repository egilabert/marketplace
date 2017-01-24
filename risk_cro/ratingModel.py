# -*- coding: utf-8 -*-
import sys  
reload(sys) 
sys.setdefaultencoding('utf8')

import pandas as pd

class RatingModel:

	def __init__(self, sector, fondos_propios, activo_corriente, 
				activo_no_corriente, pasivo_corriente, pasivo_no_corriente, 
				importe_neto_cifra_negocio, gastos_financieros, resultados_antes_impuestos):

		# --- Parametros del modelo ---
		self.sectorial_data = pd.read_csv('sectorial.csv', encoding='latin1', sep=';', decimal=',')
		self.sectores_data = pd.read_csv('sectores.csv', encoding='latin1', sep=';', decimal=',')
		self.m_activo_corriente = [1.010126, 0.6905959,	0.3511273, 0]
		self.m_ratio_autonomia_financiera = [0, 0.1646282, 0.6776536, 1.29607]
		self.m_gastos_financiera_entre_ventas = [0.9693287,	0.8044454, 0.3827373, 0]
		self.m_resultados_entre_ventas = [0, 0.2427986, 0.3750541, 0.6537845]
		self.m_grupo_sectorial = [0, 0.05615981, 0.4273994, 1.064419]
		self.m_independiente = -0.2205067

		# --- Variables de entrada ---
		self.sector = sector
		self.fondos_propios = fondos_propios
		self.activo_corriente = activo_corriente
		self.activo_no_corriente = activo_no_corriente
		self.pasivo_corriente = pasivo_corriente
		self.pasivo_no_corriente = pasivo_no_corriente
		self.importe_neto_cifra_negocio = importe_neto_cifra_negocio
		self.gastos_financieros = gastos_financieros
		self.resultados_antes_impuestos = resultados_antes_impuestos

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
				return "C - SITUACIÓN SECTORIAL MEJORABLE".encode("utf-8")
			elif rating<2.58:
				return "B - SITUACIÓN SECTORIAL BUENA".encode("utf-8")
			else:
				return "A - SITUACIÓN SECTORIAL EXCELENTE".encode("utf-8")
		else:
			if rating<0.96:
				return "C - SITUACIÓN SECTORIAL MEJORABLE".encode("utf-8")
			elif rating<2.58:
				return "B - SITUACIÓN SECTORIAL BUENA".encode("utf-8")
			else:
				return "A - SITUACIÓN SECTORIAL EXCELENTE".encode("utf-8")

	# Motor de cálculo del rating
	def RatingModel(self):
		# Selección de datos sectoriales
		datos_sectorial = self.sectorial_data[self.sectorial_data['COD_SEC20'].isin(self.get_sector_params(self.sector)['#'].values)]
		# Cálculo de los tramos del modelo
		tramo_activo_corriente = self.get_tramo(self.activo_corriente, datos_sectorial, 'Activo_Corriente')
		tramo_r_Autonomia_Financiera = self.get_tramo(float(self.fondos_propios) / float(self.pasivo_corriente + self.pasivo_no_corriente + self.fondos_propios), datos_sectorial, 'R_Autonomia_Financiera')
		tramo_gastos_fin_entre_ventas = self.get_tramo(float(self.gastos_financieros)/float(self.importe_neto_cifra_negocio), datos_sectorial, 'R_Gastos_Financieros')
		tramo_resultados_entre_ventas = self.get_tramo(float(self.resultados_antes_impuestos)/float(self.importe_neto_cifra_negocio), datos_sectorial, 'R_Resultados_Sobre_Ventas')
		tramo_grupo_sectorial = self.tramo_grupo_sectorial()
		tramos = [tramo_activo_corriente, tramo_r_Autonomia_Financiera, tramo_gastos_fin_entre_ventas, tramo_resultados_entre_ventas, tramo_grupo_sectorial]
		rating = self.m_activo_corriente[tramo_activo_corriente-1] + self.m_ratio_autonomia_financiera[tramo_r_Autonomia_Financiera-1] + self.m_gastos_financiera_entre_ventas[tramo_gastos_fin_entre_ventas-1] + self.m_resultados_entre_ventas[tramo_resultados_entre_ventas-1] + self.m_grupo_sectorial[tramo_grupo_sectorial-1] + self.m_independiente
		return [rating, self.traduccion_rating(rating).decode('utf-8')]


x = RatingModel("Química",3408575,6856290,6423972,7433555,2438132,3030560,388767,334399)
print(x.RatingModel())
