#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recommendations_clients:
#########################################################################################################################################################3333
# Respuestas recomendaciones clientes
    # Como son mis  clientes? - Volumen de ventas
    def respuesta_clientes_ventas_info(self):
        return "El volumen de ventas equivale a la facturación a cierre de año presentada en los estados financieros. Evidentemente, puede ayudarte a poner en relación el tamaño relativo de tus clientes y su evolución"
    
    def respuesta_clientes_ventas_interpretation(self):
		if len(self.balance_clients_sells())>0:
			balance_sells_deviation = float(self.balance_clients_sells()[len(self.balance_clients_sells())-1]['c']-self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1]['c'])/float(self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1]['c'])
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
			return "No existen estados financieros del cliente"

    def respuesta_clientes_ventas_hint(self):
        balance_sells_deviation = float(self.balance_clients_sells()[len(self.balance_clients_sells())-1]['c']-self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1]['c'])/float(self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1]['c'])
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
    
    def respuesta_clientes_ventas_interpretation_delta(self):
        balance_clients_sells_delta = float(self.balance_clients_sells()[len(self.balance_clients_sells())-1]['c']-self.balance_clients_sells()[len(self.balance_clients_sells())-2]['c'])/float(self.balance_clients_sells()[len(self.balance_clients_sells())-2]['c'])
        balance_clients_sells_avg_sector_delta = float(self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1]['c']-self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-2]['c'])/float(self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-2]['c'])
        if (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > 0.5:
            return "En promedio, tus clientes están creciendo mucho más que los de tu competencia."
        elif (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > 0.1:
            return "En promedio, tus clientes están creciendo más que los de tu competencia."
        elif (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > -0.1:
            return "En promedio, tus clientes evolucionan de manera parecida a los de tu competencia."
        elif (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > -0.5:
            return "En promedio, tus clientes evolucionan peor que los de tu competencia."
        else:
            return "En promedio, tus clientes evolucionan mucho peor que los de tu competencia."

    def respuesta_clientes_ventas_hint_delta(self):
        balance_clients_sells_delta = float(self.balance_clients_sells()[len(self.balance_clients_sells())-1]['c']-self.balance_clients_sells()[len(self.balance_clients_sells())-2]['c'])/float(self.balance_clients_sells()[len(self.balance_clients_sells())-2]['c'])
        balance_clients_sells_avg_sector_delta = float(self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-1]['c']-self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-2]['c'])/float(self.balance_clients_sells_avg_sector()[len(self.balance_clients_sells_avg_sector())-2]['c'])
        if (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > 0.5:
            return "Sigue así! Parece una buena estrategia realizar acciones de fidelización e intentar crecer con los clientes actuales."
        elif (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > 0.1:
            return "Muy bien! Parece una buena estrategia realizar acciones de fidelización con los clientes actuales."
        elif (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > -0.1:
            return "Bien! Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        elif (balance_clients_sells_delta - balance_clients_sells_avg_sector_delta) > -0.5:
            return "Atención! Podrías tener dificultades para mantener tu volúmen de ventas con algunos de tus clientes. Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "Alerta! Deberías prever dificultades para mantener tu volúmen de ventas con algunos de tus clientes. Podrías realizar acciones de fidelización pero deberías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."

# Como son mis  clientes? - EBITDA
    def respuesta_clientes_ebitda_info(self):
        return "El EBITDA es la métrica habitual para medir la calidad del modelo de negocio. Evidentemente, puede ayudarte a poner en relación la calidad relativa de tus clientes y su evolución"
    
    def respuesta_clientes_ebitda_interpretation(self):
        balance_ebitda_deviation = float(self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-1]['c']-self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-1]['c'])/float(self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-1]['c'])
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

    def respuesta_clientes_ebitda_hint(self):
        balance_ebitda_deviation = float(self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-1]['c']-self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-1]['c'])/float(self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-1]['c'])
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
    
    def respuesta_clientes_ebitda_interpretation_delta(self):
        balance_clients_ebitda_delta = float(self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-1]['c']-self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-2]['c'])/float(self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-2]['c'])
        balance_clients_ebitda_avg_sector_delta = float(self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-1]['c']-self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-2]['c'])/float(self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-2]['c'])
        if (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > 0.5:
            return "En promedio, tus clientes están creciendo mucho más que los de tu competencia."
        elif (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > 0.1:
            return "En promedio, tus clientes están creciendo más que los de tu competencia."
        elif (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > -0.1:
            return "En promedio, tus clientes evolucionan de manera parecida a los de tu competencia."
        elif (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > -0.5:
            return "En promedio, tus clientes evolucionan peor que los de tu competencia."
        else:
            return "En promedio, tus clientes evolucionan mucho peor que los de tu competencia."

    def respuesta_clientes_ebitda_hint_delta(self):
        balance_clients_ebitda_delta = float(self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-1]['c']-self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-2]['c'])/float(self.balance_clients_ebitda()[len(self.balance_clients_ebitda())-2]['c'])
        balance_clients_ebitda_avg_sector_delta = float(self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-1]['c']-self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-2]['c'])/float(self.balance_clients_ebitda_avg_sector()[len(self.balance_clients_ebitda_avg_sector())-2]['c'])
        if (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > 0.5:
            return "Sigue así! Parece una buena estrategia realizar acciones de fidelización e intentar crecer con los clientes actuales."
        elif (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > 0.1:
            return "Muy bien! Parece una buena estrategia realizar acciones de fidelización con los clientes actuales."
        elif (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > -0.1:
            return "Bien! Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        elif (balance_clients_ebitda_delta - balance_clients_ebitda_avg_sector_delta) > -0.5:
            return "Atención! Podrías tener dificultades para mantener tu volúmen de ventas con algunos de tus clientes. Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "Alerta! Deberías prever dificultades para mantener tu volúmen de ventas con algunos de tus clientes. Podrías realizar acciones de fidelización pero deberías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."

# Como son mis  clientes? - REsultado de explotacion
    def respuesta_clientes_resultado_info(self):
        return "El Resultado de explotación es la métrica que mejor representa la gestión del negocio. Evidentemente, puede ayudarte a poner en relación la calidad relativa de tus clientes y su evolución."
    
    def respuesta_clientes_resultado_interpretation(self):
        balance_resultado_deviation = float(self.balance_clients_resultado()[len(self.balance_clients_resultado())-1]['c']-self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-1]['c'])/float(self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-1]['c'])
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

    def respuesta_clientes_resultado_hint(self):
        balance_resultado_deviation = float(self.balance_clients_resultado()[len(self.balance_clients_resultado())-1]['c']-self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-1]['c'])/float(self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-1]['c'])
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
    
    def respuesta_clientes_resultado_interpretation_delta(self):
        balance_clients_resultado_delta = float(self.balance_clients_resultado()[len(self.balance_clients_resultado())-1]['c']-self.balance_clients_resultado()[len(self.balance_clients_resultado())-2]['c'])/float(self.balance_clients_resultado()[len(self.balance_clients_resultado())-2]['c'])
        balance_clients_resultado_avg_sector_delta = float(self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-1]['c']-self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-2]['c'])/float(self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-2]['c'])
        if (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > 0.5:
            return "En promedio, tus clientes están creciendo mucho más que los de tu competencia."
        elif (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > 0.1:
            return "En promedio, tus clientes están creciendo más que los de tu competencia."
        elif (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > -0.1:
            return "En promedio, tus clientes evolucionan de manera parecida a los de tu competencia."
        elif (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > -0.5:
            return "En promedio, tus clientes evolucionan peor que los de tu competencia."
        else:
            return "En promedio, tus clientes evolucionan mucho peor que los de tu competencia."

    def respuesta_clientes_resultado_hint_delta(self):
        balance_clients_resultado_delta = float(self.balance_clients_resultado()[len(self.balance_clients_resultado())-1]['c']-self.balance_clients_resultado()[len(self.balance_clients_resultado())-2]['c'])/float(self.balance_clients_resultado()[len(self.balance_clients_resultado())-2]['c'])
        balance_clients_resultado_avg_sector_delta = float(self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-1]['c']-self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-2]['c'])/float(self.balance_clients_resultado_avg_sector()[len(self.balance_clients_resultado_avg_sector())-2]['c'])
        if (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > 0.5:
            return "Sigue así! Parece una buena estrategia realizar acciones de fidelización e intentar crecer con los clientes actuales."
        elif (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > 0.1:
            return "Muy bien! Parece una buena estrategia realizar acciones de fidelización con los clientes actuales."
        elif (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > -0.1:
            return "Bien! Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        elif (balance_clients_resultado_delta - balance_clients_resultado_avg_sector_delta) > -0.5:
            return "Atención! Podrías tener dificultades para mantener tu volúmen de ventas con algunos de tus clientes. Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "Alerta! Deberías prever dificultades para mantener tu volúmen de ventas con algunos de tus clientes. Podrías realizar acciones de fidelización pero deberías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."

    # Como me relaciono con ellos? - Fidelización
    def respuesta_clientes_fidelizacion_info(self):
        return "La interacción media y años de antigüedad son métricas de fielización: miden la frecuencia con que interactuas con tus clientes a través de las transferencias realizadas y los años transcurridos desde vuestra primera interacción"
    
    def respuesta_clientes_fidelizacion_interacciones_interpretation(self):
        monthly_sells_deviation = float(self.get_monthly_sells()[len(self.get_monthly_sells())-1]['c']-self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1]['c'])/float(self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1]['c'])
        if monthly_sells_deviation > 0.20:
            return "En promedio, interactúas más veces con tus clientes que la competencia con los suyos."
        elif monthly_sells_deviation > -0.20:
            return "En promedio, interactúas con tus clientes de manera parecida a tu competencia con los suyos."
        else:
            return "En promedio, interactúas menos veces con tus clientes que la competencia con los suyos."

    def respuesta_clientes_fidelizacion_interacciones_hint(self):
        monthly_sells_deviation = float(self.get_monthly_sells()[len(self.get_monthly_sells())-1]['c']-self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1]['c'])/float(self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1]['c'])
        if monthly_sells_deviation > 0.20:
            return "Sigue así! Interactuar a menudo con los clientes es una buena métrica de fidelización, aunque tal vez implique mayor carga administrativa para tu empresa."
        elif monthly_sells_deviation > -0.20:
            return "Bien! No apreciamos diferencias significativas con la media de tu sector."
        else:
            return "Atención! Interactuar poco con los clientes suele aumentar el riesgo de fuga. Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
    
    #####FALTAN LAS METRICAS DE ANTIGUEDAD, QUE SON FALSAS 

# Como me relaciono con ellos? - Frecuencia
    def respuesta_clientes_frecuenca_info(self):
        return "El histograma muestra el volumen de compras de tus clientes y los de tu competencia mes a mes, permitiendo identificar fortalezas y/o oportunidades comerciales en distintos momentos del año."
    
    def respuesta_clientes_frecuencia_interpretation(self):
        #hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()[len(self.hhi_temporal_clients())-1]['c']-self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])/float(self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])
        hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        if hhi_temporal_clients_deviation > 0.50:
            return "Tus clientes tienen una mayor estacionalidad en su ciclo de compras que los clientes de tu competencia."
        elif hhi_temporal_clients_deviation > -0.50:
            return "Tus clientes tienen una estacionalidad parecida en su ciclo de compras que los clientes de tu competencia."
        else:
            return "Tus clientes tienen una menor estacionalidad en su ciclo de compras que los clientes de tu competencia."

    def respuesta_clientes_frecuencia_hint(self):
        #hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()[len(self.hhi_temporal_clients())-1]['c']-self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])/float(self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])
        hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())     
        if hhi_temporal_clients_deviation > 0.50:
            return "Atención! Parece una buena estrategia realizar disminuir el riesgo de estacionalidad implícito en tu cartera de clientes. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        elif hhi_temporal_clients_deviation > -0.50:
            return "Bien! Si quieres reducir el riesgo de estacionalidad implícito en tu cartera de clientes puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "Sigue así! Parece que consigues diversificar tu actividad una buena estrategia realizar disminuir el riesgo de estacionalidad implícito en tu cartera de clientes. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
    #####OJO! No lo pinta por algun error que todavia no se ver...

# Como me relaciono con ellos? - Penetración
    def respuesta_clientes_penetracion_info(self):
        return "El porcentaje de penetración mide el volumen de tu facturación con tus clientes sobre el total de gasto de los clientes; su varianza, indica el cambio respecto al periodo anterior."
    
    def respuesta_clientes_penetracion_interpretation(self):
        #my_penetration_client_deviation = float(self.my_penetration_client()[len(self.my_penetration_client())-1]['c']-self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])/float(self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])
        my_penetration_client_deviation = float(self.my_penetration_client()-self.my_sector_penetration_client())/float(self.my_sector_penetration_client())
        if my_penetration_client_deviation > 0.50:
            return "En promedio, eres un proveedor muy relevante para tus clientes."
        elif my_penetration_client_deviation > -0.50:
            return "En promedio, eres un proveedor relevante para tus clientes."
        else:
            return "En promedio, eres un proveedor poco relevante para tus clientes."

    def respuesta_clientes_penetracion_hint(self):
        #my_penetration_client_deviation = float(self.my_penetration_client()[len(self.my_penetration_client())-1]['c']-self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])/float(self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])
        my_penetration_client_deviation = float(self.my_penetration_client()-self.my_sector_penetration_client())/float(self.my_sector_penetration_client())
        if my_penetration_client_deviation > 0.50:
            return "Sigue así! Es importante mantener la alta fidelización de tus clientes, pero tienes menos posibilidades de crecer con ellos. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        elif my_penetration_client_deviation > -0.50:
            return "Bien! Es importante mantener la alta fidelización de tus clientes e intentar crecer con ellos. También puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "Atención! Deberías tener oportunidades de crecer en tus clientes. También puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
    #####FALTAN LAS VARIACIONES....incluir?

# Debería buscar nuevas ooportunidades? - Índices de concentración

    def respuesta_clientes_concentracion_info(self):
        return "Los índices de concentración miden, en una escala 0-1, la concentración de tu facturación según criterio de clientes, geográfico, sectorial o temporal. Normalmente, un elevado índicie de concentración representa un mayor riesgo para el negocio."
    
    def respuesta_clientes_concentracion_interpretation(self):
        hhi_clients_clients_deviation = float(self.hhi_clients_clients()-self.hhi_clients_sector_clients())/float(self.hhi_clients_sector_clients())
        hhi_geografical_clients_deviation = float(self.hhi_geografical_clients()-self.hhi_geografical_sector_clients())/float(self.hhi_geografical_sector_clients())
        hhi_cnae_clients_deviation = float(self.hhi_cnae_clients()-self.hhi_cnae_sector_clients())/float(self.hhi_cnae_sector_clients())
        hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        hhi_critic_deviation_high = Max(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        hhi_critic_deviation_low = Min(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        #Solamente interpreto el hhi con desviación más elevada (donde tu como empresa peor estas)
        if hhi_clients_clients_deviation == hhi_critic_deviation_high:
            if hhi_clients_clients_deviation > 0.50:
                return "Tu facturación está muy concentrada en unos pocos clientes."
            elif hhi_clients_clients_deviation > -0.50:
                return "Tu facturación está razonablemente distribuida entre tus clientes."
            else:
                return "Tu facturación está bien diversificada en tus clientes."
        
        elif hhi_geografical_clients_deviation == hhi_critic_deviation_high:
            if hhi_geografical_clients_deviation > 0.50:
                return "Tu facturación está muy concentrada en una determinada geografía."
            elif hhi_geografical_clients_deviation > -0.50:
                return "Tu facturación está razonablemente distribuida en distintas geografías."
            else:
                return "Tu facturación está bien diversificada geográficamente."
        
        elif hhi_cnae_clients_deviation == hhi_critic_deviation_high:    
            if hhi_cnae_clients_deviation > 0.50:
                return "Tu facturación está muy concentrada en un determinado sector."
            elif hhi_cnae_clients_deviation > -0.50:
                return "Tu facturación está razonablemente distribuida en distintos sectores."
            else:
                return "Tu facturación está bien diversificada sectorialmente."
        
        elif hhi_temporal_clients_deviation == hhi_critic_deviation_high:    
            if hhi_temporal_clients_deviation > 0.50:
                return "Tu facturación está muy concentrada en algunas épocas del año."
            elif hhi_temporal_clients_deviation > -0.50:
                return "Tu facturación está razonablemente distribuida a lo largo del año."
            else:
                return "Tu facturación está bien diversificada a lo largo del año."

    def respuesta_clientes_concentracion_hint(self):
        hhi_clients_clients_deviation = float(self.hhi_clients_clients()-self.hhi_clients_sector_clients())/float(self.hhi_clients_sector_clients())
        hhi_geografical_clients_deviation = float(self.hhi_geografical_clients()-self.hhi_geografical_sector_clients())/float(self.hhi_geografical_sector_clients())
        hhi_cnae_clients_deviation = float(self.hhi_cnae_clients()-self.hhi_cnae_sector_clients())/float(self.hhi_cnae_sector_clients())
        hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        hhi_critic_deviation_high = Max(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        hhi_critic_deviation_low = Min(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        #Solamente interpreto el hhi con desviación más positiva y con desviación más negativa respecto la competencia
        if hhi_critic_deviation_high > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        elif hhi_critic_deviation_high > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        else:
            return "Sigue así! Es recomendable mantener unos índices de concentración bajos, pero podrías analizar si tienes oportunidades de crecimiento específicas. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."

# Como podria hacerlo ? - Margen de venta y/o ratio de eficiencia / ticket medio

    def respuesta_clientes_margen_info(self):
        return "El margen comercial (o el ratio de eficiencia) son métricas de calidad de los clientes y pueden darte una idea de posibles estrategias de precios con tus clientes."
    
    def respuesta_clientes_margen_interpretation(self):
        margen_comercial_clientes_deviation = float(self.margen_comercial_clientes()-self.margen_comercial_sector_clientes())/float(self.margen_comercial_sector_clientes())
        if margen_comercial_clientes_deviation > 0.50:
            return "Tus clientes tiene un margen comercial elevado y un buen ratio de eficiencia."
        elif margen_comercial_clientes_deviation > -0.50:
            return "Tus clientes tiene un margen comercial y un ratio de eficiencia razonzables."
        else:
            return "Tus clientes tiene un margen comercial estrecho y un ratio de eficiencia mejorable."

    def respuesta_clientes_margen_hint(self):
        margen_comercial_clientes_deviation = float(self.margen_comercial_clientes()-self.margen_comercial_sector_clientes())/float(self.margen_comercial_sector_clientes())
        if margen_comercial_clientes_deviation > 0.50:
            return "Sigue así! Los márgenes elevados de tus clientes mitigan posibles riesgos de disminución del negocio. Podrías considerar subir precios."
        elif margen_comercial_clientes_deviation > -0.50:
            return "Bien! Los márgenes razonables de tus clientes mitigan posibles riesgos de disminución del negocio. Deberías seguir con tu estrategia de precios."
        else:
            return "Atención! Los márgenes estrechos de tus clientes pueden llevarles a buscar una reducción de costes. Podrías intensificar tus acciones de fidelización y considerar la posibilidad de ajustar tus precios."
