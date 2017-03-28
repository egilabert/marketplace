#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recommendations_market_risk:
###################################################################################################################################################################
# PIB Español
# -----------------------------------------
	PIB_Espana = [{"ejercicio": "2011", "c": 1070413}, {"ejercicio": "2012", "c": 1039758}, {"ejercicio": "2013", "c": 1025634}, {"ejercicio": "2014", "c": 1037025}, {"ejercicio": "2015", "c": 1075639}]

# PIB vs Tus Ventas
# -----------------------------------------
	def respuesta_markrisk_PIBvsU_info(self):
		return "La relación con el PIB estatal mide el impacto que el global de la economía tiene sobre tu negocio, proporcionando un indicador de la influencia que la macroeconomía tiene sobre tus ventas"

	def respuesta_markrisk_PIBvsU_interpretation(self):
		return "En los últimos años has tenido una tendencia positiva descorrelacionada de la economía."

	def respuesta_markrisk_PIBvsU_hint(self):
		return "Sigue así e intenta aprovechar la mejora económica observada para aumentar tu volúmen de ventas y consolidar tus resultados."

# PIB vs Ventas de la comptencia
# -----------------------------------------
	def respuesta_markrisk_PIBvsComp_info(self):
		return "La relación de las ventas de tu competencia con el PIB estatal mide el impacto que el global de la economía tiene sobre tu sector/actividad, de este modo podràs tener una idea de si has realizado un buen trabajo o no."

	def respuesta_markrisk_PIBvsComp_interpretation(self):
		return "Los resultados de los últimos años han sido erráticos y descorrelacionados con la competencia."

	def respuesta_markrisk_PIBvsComp_hint(self):
		return "Si bien tu comportamiento ha sido más estable y siempre positivo, tu competencia ha crecido más en el último año."

# Volumen de ventas
# -----------------------------------------
	def respuesta_ventas_info(self):
		return "El volumen de ventas equivale a la facturación a cierre de año presentada en los estados financieros. Evidentemente, puede ayudarte a poner en relación el tamaño relativo de tus clientes y su evolución"

	def respuesta_ventas_interpretation(self):
		if self.id!=990 and self.balance_sells_avg_sector()>0:
			balance_sells_deviation = float(self.balance_sells()[len(self.balance_sells())-1]['c']-self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c'])/abs(float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c']))
			if balance_sells_deviation > 0.5:
				return "En promedio, trabajas con clientes mucho más grandes que tu competencia"
			elif balance_sells_deviation > 0.1:
				return "En promedio, trabajas con clientes más grandes que la competencia."
			elif balance_sells_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_sells_deviation > -0.5:
				return "En promedio, trabajas con clientes más pequeños que tu competencia."
			else:
				return "En promedio, trabajas con clientes mucho más pequeños que tu competencia"
		elif len(self.balance_sells())>0:
			sells_sector = self.balance_sells_avg_sector()
			sells_me = [{'ejercicio': u'2012', 'c': 1572798.16}, {'ejercicio': u'2013', 'c': 1577516.5589742612}, {'ejercicio': u'2014', 'c': 1715817.3709565657}]
			balance_sells_deviation = float(sells_me[len(sells_me)-1]['c']-sells_sector[len(sells_sector)-1]['c'])/abs(float(sells_sector[len(sells_sector)-1]['c'])) #float(self.balance_sells()[len(self.balance_sells())-1]['c']-self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c'])/abs(float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c']))
			if balance_sells_deviation > 0.5:
				return "En promedio, trabajas con clientes mucho más grandes que tu competencia"
			elif balance_sells_deviation > 0.1:
				return "En promedio, trabajas con clientes más grandes que la competencia."
			elif balance_sells_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_sells_deviation > -0.5:
				return "En promedio, trabajas con clientes más pequeños que tu competencia."
			else:
				return "En promedio, trabajas con clientes mucho más pequeños que tu competencia"
		else:
			return "No disponemos de datos financieros"


	def respuesta_ventas_hint(self):
		if self.id!=990 and self.balance_sells_avg_sector()>0:
			balance_sells_deviation = float(self.balance_sells()[len(self.balance_sells())-1]['c']-self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c'])/abs(float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c']))
			if balance_sells_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_sells_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_sells_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar clientes de mayor tamaño utilizando nuestro motor de recomendaciones."
			elif balance_sells_deviation > -0.5:
				return "Atención! Trabajar con clientes más pequeños encarece los procesos comerciales y dificulta la escalabilidad del negocio. Has probado con clientes más grandes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes muy pequeños encarece los procesos comerciales y dificulta la escalabilidad del negocio. Has probado con clientes más grandes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		elif len(self.balance_sells())>0:
			sells_sector = self.balance_sells_avg_sector()
			sells_me = [{'ejercicio': u'2012', 'c': 1572798.16}, {'ejercicio': u'2013', 'c': 1577516.5589742612}, {'ejercicio': u'2014', 'c': 1715817.3709565657}]
			balance_sells_deviation = float(sells_me[len(sells_me)-1]['c']-sells_sector[len(sells_sector)-1]['c'])/abs(float(sells_sector[len(sells_sector)-1]['c'])) #float(self.balance_sells()[len(self.balance_sells())-1]['c']-self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c'])/abs(float(self.balance_sells_avg_sector()[len(self.balance_sells_avg_sector())-1]['c']))
			if balance_sells_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_sells_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_sells_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar clientes de mayor tamaño utilizando nuestro motor de recomendaciones."
			elif balance_sells_deviation > -0.5:
				return "Atención! Trabajar con clientes más pequeños encarece los procesos comerciales y dificulta la escalabilidad del negocio. Has probado con clientes más grandes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes muy pequeños encarece los procesos comerciales y dificulta la escalabilidad del negocio. Has probado con clientes más grandes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		else:
			return "No disponemos de datos financieros"

# EBITDA
# -----------------------------------------
	def respuesta_ebitda_info(self):
		return "El EBITDA es la métrica habitual para medir la calidad del modelo de negocio. Evidentemente, puede ayudarte a poner en relación la calidad relativa de tu negocio frente al de tu competencia"

	def respuesta_ebitda_interpretation(self):
		if self.id!=990 and self.balance_ebitda_avg_sector()>0:
			balance_ebitda_deviation = float(self.balance_ebitda()[len(self.balance_ebitda())-1]['c']-self.balance_ebitda_avg_sector()[len(self.balance_ebitda_avg_sector())-1]['c'])/abs(float(self.balance_ebitda_avg_sector()[len(self.balance_ebitda_avg_sector())-1]['c']))
			if balance_ebitda_deviation > 0.5:
				return "En promedio, trabajas con clientes mucho más fuertes que tu competencia"
			elif balance_ebitda_deviation > 0.1:
				return "En promedio, trabajas con clientes más fuertes que la competencia."
			elif balance_ebitda_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_ebitda_deviation > -0.5:
				return "En promedio, trabajas con clientes más débiles que tu competencia."
			else:
				return "En promedio, trabajas con clientes mucho más débiles que tu competencia"
		elif len(self.balance_ebitda())>0:
			ebitda_sector = self.balance_ebitda_avg_sector()
			ebitda_me = [{'ejercicio': u'2012', 'c': 43398.89}, {'ejercicio': u'2013', 'c': 47000.31050235448}, {'ejercicio': u'2014', 'c': 49390.84002892549}]
			balance_ebitda_deviation = float(ebitda_me[len(ebitda_me)-1]['c']-ebitda_sector[len(ebitda_sector)-1]['c'])/abs(float(ebitda_sector[len(ebitda_sector)-1]['c']))
			if balance_ebitda_deviation > 0.5:
				return "En promedio, trabajas con clientes mucho más fuertes que tu competencia"
			elif balance_ebitda_deviation > 0.1:
				return "En promedio, trabajas con clientes más fuertes que la competencia."
			elif balance_ebitda_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_ebitda_deviation > -0.5:
				return "En promedio, trabajas con clientes más débiles que tu competencia."
			else:
				return "En promedio, trabajas con clientes mucho más débiles que tu competencia"
		else:
			return "No disponemos de datos financieros"

	def respuesta_ebitda_hint(self):
		if self.id!=990 and self.balance_ebitda_avg_sector()>0:
			balance_ebitda_deviation = float(self.balance_ebitda()[len(self.balance_ebitda())-1]['c']-self.balance_ebitda_avg_sector()[len(self.balance_ebitda_avg_sector())-1]['c'])/abs(float(self.balance_ebitda_avg_sector()[len(self.balance_ebitda_avg_sector())-1]['c']))
			if balance_ebitda_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebitda_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebitda_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar clientes más  fuertes utilizando nuestro motor de recomendaciones."
			elif balance_ebitda_deviation > -0.5:
				return "Atención! Trabajar con clientes más débiles es más arriesgado para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes en dificultades supone un riesgo para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		elif len(self.balance_ebitda())>0:
			ebitda_sector = self.balance_ebitda_avg_sector()
			ebitda_me = [{'ejercicio': u'2012', 'c': 43398.89}, {'ejercicio': u'2013', 'c': 47000.31050235448}, {'ejercicio': u'2014', 'c': 49390.84002892549}]
			balance_ebitda_deviation = float(ebitda_me[len(ebitda_me)-1]['c']-ebitda_sector[len(ebitda_sector)-1]['c'])/abs(float(ebitda_sector[len(ebitda_sector)-1]['c']))
			if balance_ebitda_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebitda_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebitda_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar clientes más  fuertes utilizando nuestro motor de recomendaciones."
			elif balance_ebitda_deviation > -0.5:
				return "Atención! Trabajar con clientes más débiles es más arriesgado para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes en dificultades supone un riesgo para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		else:
			return "No disponemos de datos financieros"

# EBIT
# -----------------------------------------
	def respuesta_ebit_info(self):
		return "El EBIT es la métrica habitual para medir la calidad del modelo de negocio. Evidentemente, puede ayudarte a poner en relación la calidad relativa de tu negocio frente al de tu competencia"

	def respuesta_ebit_interpretation(self):
		if self.id!=990 and self.balance_ebit_avg_sector()>0:
			balance_ebit_deviation = float(self.balance_ebit()[len(self.balance_ebit())-1]['c']-self.balance_ebit_avg_sector()[len(self.balance_ebit_avg_sector())-1]['c'])/abs(float(self.balance_ebit_avg_sector()[len(self.balance_ebit_avg_sector())-1]['c']))
			if balance_ebit_deviation > 0.5:
				return "En promedio, trabajas con clientes mucho más fuertes que tu competencia"
			elif balance_ebit_deviation > 0.1:
				return "En promedio, trabajas con clientes más fuertes que la competencia."
			elif balance_ebit_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_ebit_deviation > -0.5:
				return "En promedio, trabajas con clientes más débiles que tu competencia."
			else:
				return "En promedio, trabajas con clientes mucho más débiles que tu competencia"
		elif len(self.balance_ebit())>0:
			ebit_sector = self.balance_ebit_avg_sector()
			ebit_me = [{'ejercicio': u'2012', 'c': 33242.47}, {'ejercicio': u'2013', 'c': 33111.16488357351}, {'ejercicio': u'2014', 'c': 38091.645286164814}]
			balance_ebit_deviation = float(ebit_me[len(ebit_me)-1]['c']-ebit_sector[len(ebit_sector)-1]['c'])/abs(float(ebit_sector[len(ebit_sector)-1]['c']))
			if balance_ebit_deviation > 0.5:
				return "En promedio, trabajas con clientes mucho más fuertes que tu competencia"
			elif balance_ebit_deviation > 0.1:
				return "En promedio, trabajas con clientes más fuertes que la competencia."
			elif balance_ebit_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_ebit_deviation > -0.5:
				return "En promedio, trabajas con clientes más débiles que tu competencia."
			else:
				return "En promedio, trabajas con clientes mucho más débiles que tu competencia"
		else:
			return "No disponemos de datos financieros"

	def respuesta_ebit_hint(self):
		if self.id!=990 and self.balance_ebit_avg_sector()>0:
			balance_ebit_deviation = float(self.balance_ebit()[len(self.balance_ebit())-1]['c']-self.balance_ebit_avg_sector()[len(self.balance_ebit_avg_sector())-1]['c'])/abs(float(self.balance_ebit_avg_sector()[len(self.balance_ebit_avg_sector())-1]['c']))
			if balance_ebit_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebit_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebit_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar clientes más  fuertes utilizando nuestro motor de recomendaciones."
			elif balance_ebit_deviation > -0.5:
				return "Atención! Trabajar con clientes más débiles es más arriesgado para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes en dificultades supone un riesgo para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		elif len(self.balance_ebit())>0:
			ebit_sector = self.balance_ebit_avg_sector()
			ebit_me = [{'ejercicio': u'2012', 'c': 33242.47}, {'ejercicio': u'2013', 'c': 33111.16488357351}, {'ejercicio': u'2014', 'c': 38091.645286164814}]
			balance_ebit_deviation = float(ebit_me[len(ebit_me)-1]['c']-ebit_sector[len(ebit_sector)-1]['c'])/abs(float(ebit_sector[len(ebit_sector)-1]['c']))
			if balance_ebit_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebit_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_ebit_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar clientes más  fuertes utilizando nuestro motor de recomendaciones."
			elif balance_ebit_deviation > -0.5:
				return "Atención! Trabajar con clientes más débiles es más arriesgado para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes en dificultades supone un riesgo para tu negocio. Has probado con clientes más fuertes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		else:
			return "No disponemos de datos financieros"

# Resultados de explotación 
# -----------------------------------------
	def respuesta_resultado_info(self):
		return "El Resultado de explotación es la métrica que mejor representa la gestión del negocio. Evidentemente, puede ayudarte a poner en relación la calidad relativa de tu negocio frente a la de tu competencia."

	def respuesta_resultado_interpretation(self):
		if self.id!=990 and self.resultado_explotacion_avg_sector()>0:
			balance_resultado_deviation = float(self.resultado_explotacion()[len(self.resultado_explotacion())-1]['c']-self.resultado_explotacion_avg_sector()[len(self.resultado_explotacion_avg_sector())-1]['c'])/abs(float(self.resultado_explotacion_avg_sector()[len(self.resultado_explotacion_avg_sector())-1]['c']))
			if balance_resultado_deviation > 0.5:
				return "En promedio, trabajas con clientes con mucho mejores resultados que tu competencia."
			elif balance_resultado_deviation > 0.1:
				return "En promedio, trabajas con clientes con mejores resultados que la competencia."
			elif balance_resultado_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_resultado_deviation > -0.5:
				return "En promedio, trabajas con clientes con peores resultados que tu competencia."
			else:
				return "En promedio, trabajas con clientes con mucho peores resultados que tu competencia."
		elif len(self.resultado_explotacion())>0:
			resultados_sector = self.resultado_explotacion_avg_sector()
			resultados_me = [{'ejercicio': u'2012', 'c': 33242.47}, {'ejercicio': u'2013', 'c': 34079.65023359921}, {'ejercicio': u'2014', 'c': 34334.615989417565}]
			balance_resultado_deviation = float(resultados_me[len(resultados_me)-1]['c']-resultados_sector[len(resultados_sector)-1]['c'])/abs(float(resultados_sector[len(resultados_sector)-1]['c']))
			if balance_resultado_deviation > 0.5:
				return "En promedio, trabajas con clientes con mucho mejores resultados que tu competencia."
			elif balance_resultado_deviation > 0.1:
				return "En promedio, trabajas con clientes con mejores resultados que la competencia."
			elif balance_resultado_deviation > -0.1:
				return "En promedio, trabajas con clientes parecidos a los de tu competencia."
			elif balance_resultado_deviation > -0.5:
				return "En promedio, trabajas con clientes con peores resultados que tu competencia."
			else:
				return "En promedio, trabajas con clientes con mucho peores resultados que tu competencia."
		else:
			return "No disponemos de datos financieros"

	def respuesta_resultado_hint(self):
		if self.id!=990 and self.resultado_explotacion_avg_sector()>0:
			balance_resultado_deviation = float(self.resultado_explotacion()[len(self.resultado_explotacion())-1]['c']-self.resultado_explotacion_avg_sector()[len(self.resultado_explotacion_avg_sector())-1]['c'])/abs(float(self.resultado_explotacion_avg_sector()[len(self.resultado_explotacion_avg_sector())-1]['c']))
			if balance_resultado_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_resultado_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_resultado_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar mejores clientes utilizando nuestro motor de recomendaciones."
			elif balance_resultado_deviation > -0.5:
				return "Atención! Trabajar con clientes con peores resultados es más arriesgado para tu negocio. Has probado con otros clientes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes en dificultades supone un riesgo para tu negocio. Has probado con otros clientes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		if len(self.resultado_explotacion())>0:
			resultados_sector = self.resultado_explotacion_avg_sector()
			resultados_me = [{'ejercicio': u'2012', 'c': 33242.47}, {'ejercicio': u'2013', 'c': 34079.65023359921}, {'ejercicio': u'2014', 'c': 34334.615989417565}]
			balance_resultado_deviation = float(resultados_me[len(resultados_me)-1]['c']-resultados_sector[len(resultados_sector)-1]['c'])/abs(float(resultados_sector[len(resultados_sector)-1]['c']))
			if balance_resultado_deviation > 0.5:
				return "Sigue así! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_resultado_deviation > 0.1:
				return "Muy bien! Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			elif balance_resultado_deviation > -0.1:
				return "Bien! Si te interesa, puedes encontrar mejores clientes utilizando nuestro motor de recomendaciones."
			elif balance_resultado_deviation > -0.5:
				return "Atención! Trabajar con clientes con peores resultados es más arriesgado para tu negocio. Has probado con otros clientes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
			else:
				return "Alerta! Trabajar con clientes en dificultades supone un riesgo para tu negocio. Has probado con otros clientes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
		else:
			return "No disponemos de datos financieros"