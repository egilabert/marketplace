#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recommendations_providers:
###################################################################################################################################################################
# Respuestas recomendaciones proveeedores
    # Como son mis proveedores? - Volumen de ventas

    #  OJO!!! Estamos pintando gasto....pero utilizamos este grafico como métrica de tam´ño de los proveedores. Creo que deberiamos volver a VENTAS
    def respuesta_providers_ventas_info(self):
        return "El volumen de ventas equivale a la facturación a cierre de año presentada en los estados financieros. Evidentemente, puede ayudarte a poner en relación el tamaño relativo de tus clientes."
    
    def respuesta_providers_ventas_interpretation(self):
        if self.id==1610:
            return "En promedio, trabajas con proveedores más grandes que la competencia."
        elif len(self.balance_providers_sells())>0:
            balance_sells_deviation = float(self.balance_providers_sells()[len(self.balance_providers_sells())-1]['c']-self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-1]['c'])/float(self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-1]['c'])
            if balance_sells_deviation > 0.5:
                return "En promedio, trabajas con proveedores mucho más grandes que tu competencia"
            elif balance_sells_deviation > 0.1:
                return "En promedio, trabajas con proveedores más grandes que la competencia."
            elif balance_sells_deviation > -0.1:
                return "En promedio, trabajas con proveedores parecidos a los de tu competencia."
            elif balance_sells_deviation > -0.5:
                return "En promedio, trabajas con proveedores más pequeños que tu competencia."
            else:
                return "En promedio, trabajas con proveedores mucho más pequeños que tu competencia"
        else:
            return "No disponemos de tus datos financieros"

    def respuesta_providers_ventas_hint(self):
        if self.id==1610:
            return "Muy bien! Si buscas ampliar tu base de proveedores utiliza nuestro motor de recomendaciones."
        elif len(self.balance_providers_sells())>0:
            balance_sells_deviation = float(self.balance_providers_sells()[len(self.balance_providers_sells())-1]['c']-self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-1]['c'])/float(self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-1]['c'])
            if balance_sells_deviation > 0.5:
                return "Sigue así! Si buscas ampliar tu base de proveedores utiliza nuestro motor de recomendaciones."
            elif balance_sells_deviation > 0.1:
                return "Muy bien! Si buscas ampliar tu base de proveedores utiliza nuestro motor de recomendaciones."
            elif balance_sells_deviation > -0.1:
                return "Bien! Si te interesa, puedes encontrar proveedores de mayor tamaño utilizando nuestro motor de recomendaciones."
            elif balance_sells_deviation > -0.5:
                return "Atención! Trabajar con proveedores más pequeños te da mayor poder de negociación pero puede aumentar el riesgo para tu empresa. Has probado con proveedores más grandes? Si buscas nuevas oportunidades comerciales utiliza nuestro motor de recomendaciones."
            else:
                return "Alerta! Trabajar con proveedores muy pequeños da mayor poder de negociación pero puede aumentar el riesgo para tu empresa. Has probado con proveedores más grandes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones."
        else:
            return "No disponemos de tus datos financieros"
    

    def respuesta_providers_ventas_interpretation_delta(self):
        if len(self.balance_providers_sells())>1:
            balance_providers_sells_delta = float(self.balance_providers_sells()[len(self.balance_providers_sells())-1]['c']-self.balance_providers_sells()[len(self.balance_providers_sells())-2]['c'])/float(self.balance_providers_sells()[len(self.balance_providers_sells())-2]['c'])
            balance_providers_sells_avg_sector_delta = float(self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-1]['c']-self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-2]['c'])/float(self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-2]['c'])
            if (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > 0.5:
                return "En promedio, tus proveedores están creciendo mucho más que los de tu competencia."
            elif (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > 0.1:
                return "En promedio, tus proveedores están creciendo más que los de tu competencia."
            elif (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > -0.1:
                return "En promedio, tus proveedores evolucionan de manera parecida a los de tu competencia."
            elif (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > -0.5:
                return "En promedio, tus proveedores evolucionan peor que los de tu competencia."
            else:
                return "En promedio, tus proveedores evolucionan mucho peor que los de tu competencia."
        else:
            return "No disponemos de histórico de tus datos financieros para medir la evolución"

    def respuesta_providers_ventas_hint_delta(self):
        if len(self.balance_providers_sells())>1:
            balance_providers_sells_delta = float(self.balance_providers_sells()[len(self.balance_providers_sells())-1]['c']-self.balance_providers_sells()[len(self.balance_providers_sells())-2]['c'])/float(self.balance_providers_sells()[len(self.balance_providers_sells())-2]['c'])
            balance_providers_sells_avg_sector_delta = float(self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-1]['c']-self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-2]['c'])/float(self.balance_providers_sells_avg_sector()[len(self.balance_providers_sells_avg_sector())-2]['c'])
            if (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > 0.5:
                return "Sigue así! Parece que el mercado está confiando mucho más en tus proveedores actuales."
            elif (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > 0.1:
                return "Muy bien! Parece que el mercado está confiando más en tus proveedores actuales."
            elif (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > -0.1:
                return "Bien! Parece que el mercado sigue confiando en tus proveedores actuales."
            elif (balance_providers_sells_delta - balance_providers_sells_avg_sector_delta) > -0.5:
                return "Atención! Tus proveedores han disminuido significativamente sus ventas y podrían estar entrando en un periodo de dificultades. Puedes intentar ampliar tu base de proveedores utilizando nuestro motor de recomendaciones."
            else:
                return "Alerta! Tus proveedores podrían estar entrando en un periodo de serias dificultades. Puedes intentar ampliar tu base de proveedores utilizando nuestro motor de recomendaciones."
        else:
            return "No disponemos de histórico de tus datos financieros para medir la evolución"

# Como son mis  clientes? - EBITDA
    def respuesta_providers_ebitda_info(self):
        return "El EBITDA es la métrica habitual para medir la calidad del modelo de negocio. Evidentemente, puede ayudarte a poner en relación la calidad relativa de tus clientes y su evolución"
    
    def respuesta_providers_ebitda_interpretation(self):
        if self.id==1610:
            return "En promedio, trabajas con proveedores más fuertes que la competencia."
        elif len(self.balance_providers_ebitda())>0:
            balance_ebitda_deviation = float(self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-1]['c']-self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-1]['c'])/abs(float(self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-1]['c']))
            if balance_ebitda_deviation > 0.5:
                return "En promedio, trabajas con proveedores mucho más fuertes que tu competencia."
            elif balance_ebitda_deviation > 0.1:
                return "En promedio, trabajas con proveedores más fuertes que la competencia."
            elif balance_ebitda_deviation > -0.1:
                return "En promedio, trabajas con proveedores parecidos a los de tu competencia."
            elif balance_ebitda_deviation > -0.5:
                return "En promedio, trabajas con proveedores más débiles que tu competencia."
            else:
                return "En promedio, trabajas con proveedores mucho más débiles que tu competencia."
        else:
            return "No disponemos de tus datos financieros"

    def respuesta_providers_ebitda_hint(self):
        if self.id==1610:
            return "Muy bien! Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones ."
        elif len(self.balance_providers_ebitda())>0:
            balance_ebitda_deviation = float(self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-1]['c']-self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-1]['c'])/abs(float(self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-1]['c']))
            if balance_ebitda_deviation > 0.5:
                return "Sigue así! Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones ."
            elif balance_ebitda_deviation > 0.1:
                return "Muy bien! Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones ."
            elif balance_ebitda_deviation > -0.1:
                return "Bien! Si te interesa, puedes encontrar proveedores más fuertes utilizando nuestro motor de recomendaciones ."
            elif balance_ebitda_deviation > -0.5:
                return "Atención! Trabajar con proveedores más débiles es más arriesgado para tu negocio. Has probado con proveedores más fuertes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones ."
            else:
                return "Alerta! Trabajar con proveedores en dificultades supone un riesgo para tu negocio. Has probado con proveedores más fuertes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones ."
        else:
            return "No disponemos de tus datos financieros"

    def respuesta_providers_ebitda_interpretation_delta(self):
        if len(self.balance_providers_ebitda())>1:
            balance_providers_ebitda_delta = float(self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-1]['c']-self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-2]['c'])/float(self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-2]['c'])
            balance_providers_ebitda_avg_sector_delta = float(self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-1]['c']-self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-2]['c'])/float(self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-2]['c'])
            if (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > 0.5:
                return "En promedio, tus proveedores están creciendo mucho más que los de tu competencia."
            elif (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > 0.1:
                return "En promedio, tus proveedores están creciendo más que los de tu competencia."
            elif (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > -0.1:
                return "En promedio, tus proveedores evolucionan de manera parecida a los de tu competencia."
            elif (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > -0.5:
                return "En promedio, tus proveedores evolucionan peor que los de tu competencia."
            else:
                return "En promedio, tus proveedores evolucionan mucho peor que los de tu competencia."
        else:
            return "No disponemos de histórico de tus datos financieros para medir la evolución"

    def respuesta_providers_ebitda_hint_delta(self):
        if len(self.balance_providers_ebitda())>1:
            balance_providers_ebitda_delta = float(self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-1]['c']-self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-2]['c'])/float(self.balance_providers_ebitda()[len(self.balance_providers_ebitda())-2]['c'])
            balance_providers_ebitda_avg_sector_delta = float(self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-1]['c']-self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-2]['c'])/float(self.balance_providers_ebitda_avg_sector()[len(self.balance_providers_ebitda_avg_sector())-2]['c'])
            if (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > 0.5:
                return "Sigue así! Parece una buena estrategia mantener tus proveedores actuales. Has probado a renegociar sus precios?."
            elif (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > 0.1:
                return "Muy bien! Parece una buena estrategia mantener tus proveedores actuales. Has probado a renegociar sus precios?."
            elif (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > -0.1:
                return "Bien! Parece una buena estrategia mantener tus proveedores actuales y no detectamos mucho margen a la reducción de precios."
            elif (balance_providers_ebitda_delta - balance_providers_ebitda_avg_sector_delta) > -0.5:
                return "Atención! Tus proveedores podrían estar entrando en dificultades. Parece una buena estrategia intentar ampliar tu base de proveedores utilizando nuestro motor de recomendaciones."
            else:
                return "Alerta! Trabajar con proveedores en dificultades supone un riesgo para tu negocio. Has probado con proveedores más fuertes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones."
        else:
            return "No disponemos de histórico de tus datos financieros para medir la evolución"

# Como son mis  clientes? - REsultado de explotacion
    def respuesta_providers_resultado_info(self):
        return "El Resultado de explotación es la métrica que mejor representa la gestión del negocio. Evidentemente, puede ayudarte a poner en relación la calidad relativa de tus proveedores y su evolución."
    
    def respuesta_providers_resultado_interpretation(self):
        if len(self.balance_providers_resultado())>0:
            balance_resultado_deviation = float(self.balance_providers_resultado()[len(self.balance_providers_resultado())-1]['c']-self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-1]['c'])/abs(float(self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-1]['c']))
            if balance_resultado_deviation > 0.5:
                return "En promedio, trabajas con proveedores con mucho mejores resultados que tu competencia."
            elif balance_resultado_deviation > 0.1:
                return "En promedio, trabajas con proveedores con mejores resultados que la competencia."
            elif balance_resultado_deviation > -0.1:
                return "En promedio, trabajas con proveedores parecidos a los de tu competencia."
            elif balance_resultado_deviation > -0.5:
                return "En promedio, trabajas con proveedores con peores resultados que tu competencia."
            else:
                return "En promedio, trabajas con proveedores con mucho peores resultados que tu competencia."
        else:
            return "No disponemos de tus datos financieros"

    def respuesta_providers_resultado_hint(self):
        if len(self.balance_providers_resultado())>0:
            balance_resultado_deviation = float(self.balance_providers_resultado()[len(self.balance_providers_resultado())-1]['c']-self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-1]['c'])/abs(float(self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-1]['c']))
            if balance_resultado_deviation > 0.5:
                return "Sigue así! Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones."
            elif balance_resultado_deviation > 0.1:
                return "Muy bien! Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones."
            elif balance_resultado_deviation > -0.1:
                return "Bien! Si te interesa, puedes encontrar proveedores más fuertes utilizando nuestro motor de recomendaciones ."
            elif balance_resultado_deviation > -0.5:
                return "Atención! Trabajar con proveedores más débiles es más arriesgado para tu negocio. Has probado con proveedores más fuertes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones ."
            else:
                return "Alerta! Trabajar con proveedores en dificultades supone un riesgo para tu negocio. Has probado con proveedores más fuertes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones ."
        else:
            return "No disponemos de tus datos financieros"
    
    def respuesta_providers_resultado_interpretation_delta(self):
        if len(self.balance_providers_resultado())>1:
            balance_providers_resultado_delta = float(self.balance_providers_resultado()[len(self.balance_providers_resultado())-1]['c']-self.balance_providers_resultado()[len(self.balance_providers_resultado())-2]['c'])/float(self.balance_providers_resultado()[len(self.balance_providers_resultado())-2]['c'])
            balance_providers_resultado_avg_sector_delta = float(self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-1]['c']-self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-2]['c'])/float(self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-2]['c'])
            if (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > 0.5:
                return "En promedio, tus proveedores están creciendo mucho más que los de tu competencia."
            elif (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > 0.1:
                return "En promedio, tus proveedores están creciendo más que los de tu competencia."
            elif (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > -0.1:
                return "En promedio, tus proveedores evolucionan de manera parecida a los de tu competencia."
            elif (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > -0.5:
                return "En promedio, tus proveedores evolucionan peor que los de tu competencia."
            else:
                return "En promedio, tus proveedores evolucionan mucho peor que los de tu competencia."
        else:
            return "No disponemos de histórico de tus datos financieros para medir la evolución"      


    def respuesta_providers_resultado_hint_delta(self):
        if len(self.balance_providers_resultado())>1:
            balance_providers_resultado_delta = float(self.balance_providers_resultado()[len(self.balance_providers_resultado())-1]['c']-self.balance_providers_resultado()[len(self.balance_providers_resultado())-2]['c'])/float(self.balance_providers_resultado()[len(self.balance_providers_resultado())-2]['c'])
            balance_providers_resultado_avg_sector_delta = float(self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-1]['c']-self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-2]['c'])/float(self.balance_providers_resultado_avg_sector()[len(self.balance_providers_resultado_avg_sector())-2]['c'])
            if (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > 0.5:
                return "Sigue así! Parece una buena estrategia mantener tus proveedores actuales. Has probado a renegociar precios?"
            elif (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > 0.1:
                return "Muy bien! Parece una buena estrategia mantener tus proveedores actuales. Has probado a renegociar precios?"
            elif (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > -0.1:
                return "Bien! Parece una buena estrategia mantener tus proveedores actuales y no detectamos mucho margen a la reducción de precios.."
            elif (balance_providers_resultado_delta - balance_providers_resultado_avg_sector_delta) > -0.5:
                return "Atención! Tus proveedores podrían estar entrando en dificultades. Parece una buena estrategia intentar ampliar tu base de proveedores utilizando nuestro motor de recomendaciones."
            else:
                return "Alerta! Trabajar con proveedores en dificultades supone un riesgo para tu negocio. Has probado con proveedores más fuertes? Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones."
        else:
            return "No disponemos de histórico de tus datos financieros para medir la evolución"

    # Como me relaciono con ellos? - Fidelización
    # def respuesta_providers_fidelizacion_info(self):
    #     return "La interacción media y años de antigüedad son métricas de fielización: miden la frecuencia con que interactuas con tus clientes a través de las transferencias realizadas y los años transcurridos desde vuestra primera interacción"
    
    # def respuesta_providers_fidelizacion_interacciones_interpretation(self):
    #     monthly_buys_deviation = float(self.get_monthly_sells()[len(self.get_monthly_sells())-1]['c']-self.get_monthly_sector_avg_sells())[len(self.get_monthly_sector_avg_sells())-1]['c'])/float(self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1]['c'])
    #     if monthly_buys_deviation > 0.20:
    #         return "En promedio, interactúas más veces con tus clientes que la competencia con los suyos."
    #     elif monthly_buys_deviation > -0.20:
    #         return "En promedio, interactúas con tus clientes de manera parecida a tu competencia con los suyos."
    #     else:
    #         return "En promedio, interactúas menos veces con tus clientes que la competencia con los suyos."

    # def respuesta_providers_fidelizacion_interacciones_hint(self):
    #     monthly_buys_deviation = float(self.get_monthly_sells()[len(self.get_monthly_sells())-1]['c']-self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1]['c'])/float(self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1]['c'])
    #     if monthly_buys_deviation > 0.20:
    #         return "Sigue así! Interactuar a menudo con los clientes es una buena métrica de fidelización, aunque tal vez implique mayor carga administrativa para tu empresa."
    #     elif monthly_buys_deviation > -0.20:
    #         return "Bien! No apreciamos diferencias significativas con la media de tu sector."
    #     else:
    #         return "Atención! Interactuar poco con los clientes suele aumentar el riesgo de fuga. Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
    
    ##### ATENCION! REVISAR LOS get_monthly_buys? sells? 
    #####FALTAN LAS METRICAS DE ANTIGUEDAD, QUE SON FALSAS 

# Como me relaciono con ellos? - Frecuencia
    def respuesta_providers_frecuenca_info(self):
        return "El histograma muestra el volumen de ventas de tus proveedores y los de tu competencia mes a mes, permitiendo identificar fortalezas y/o oportunidades comerciales en distintos momentos del año."
    
    def respuesta_providers_frecuencia_interpretation(self):
        #hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()[len(self.hhi_temporal_clients())-1]['c']-self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])/float(self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])
        hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        if hhi_temporal_providers_deviation > 0.50:
            return "Tus proveedores tienen una mayor estacionalidad en su ciclo de ventas que los proveedores de tu competencia"
        elif hhi_temporal_providers_deviation > -0.50:
            return "Tus proveedores tienen una estacionalidad parecida en su ciclo de ventas que los proveedores de tu competencia"
        else:
            return "Tus proveedores tienen una menor estacionalidad en su ciclo de ventas que los proveedores de tu competencia"

    def respuesta_providers_frecuencia_hint(self):
        #hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()[len(self.hhi_temporal_clients())-1]['c']-self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])/float(self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])
        hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        if hhi_temporal_providers_deviation > 0.50:
            return "Atención! Parece una buena estrategia realizar disminuir el riesgo de estacionalidad implícito en tu cartera de clientes. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        elif hhi_temporal_providers_deviation > -0.50:
            return "Bien! Si quieres reducir el riesgo de estacionalidad implícito en tu cartera de clientes puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "Sigue así! Parece que consigues diversificar tu actividad una buena estrategia realizar disminuir el riesgo de estacionalidad implícito en tu cartera de clientes. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
    #####OJO! No lo pinta por algun error que todavia no se ver...
    ## OJO, he cambiado ventas por compras en este apartado entero

# Como me relaciono con ellos? - Penetración
    def respuesta_providers_penetracion_info(self):
        return "El porcentaje de penetración mide el volumen de tu facturación con tus proveedores sobre el total de ventas de los proveedores; su varianza, indica el cambio respecto al periodo anterior."
    
    def respuesta_providers_penetracion_interpretation(self):
        if len(self.balance_providers_ebitda())>0:
            #my_penetration_client_deviation = float(self.my_penetration_client()[len(self.my_penetration_client())-1]['c']-self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])/float(self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])
            my_penetration_providers_deviation = float(self.my_penetration_provider()-self.my_sector_penetration_provider())/float(self.my_sector_penetration_provider())
            if my_penetration_providers_deviation > 0.50:
                return "En promedio, eres un cliente muy relevante para tus proveedores"
            elif my_penetration_providers_deviation > -0.50:
                return "En promedio, eres un cliente relevante para tus proveedores"
            else:
                return "En promedio, eres un cliente poco relevante para tus proveedores"
        else:
            return "No disponemos de tus datos financieros"

    def respuesta_providers_penetracion_hint(self):
        if len(self.balance_providers_ebitda())>0:
            #my_penetration_client_deviation = float(self.my_penetration_client()[len(self.my_penetration_client())-1]['c']-self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])/float(self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])
            my_penetration_providers_deviation = float(self.my_penetration_provider()-self.my_sector_penetration_provider())/float(self.my_sector_penetration_provider())
            if my_penetration_providers_deviation > 0.50:
                return "Sigue así! Es importante aumentar tu relevancia con los proveedores para aumentar tu poder de negociación. Has pensado en aumentar tus precios?  Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones "
            elif my_penetration_providers_deviation > -0.50:
                return "Bien! Es importante aumentar tu relevancia con los proveedores para aumentar tu poder de negociación. Si buscas ampliar  tu base de proveedores utiliza nuestro motor de recomendaciones"
            else:
                return "Atención! Parece que no eres muy relevante para tus proveedores, lo cual podría limitar tu poder de negociación. Si buscas ampliar tu base de proveedores utiliza nuestro motor de recomendaciones"
        else:
            return "No disponemos de tus datos financieros"
    #####FALTAN LAS VARIACIONES....incluir?
    #####Atención: revisar métrica my_sector_penetration_provider

# Debería buscar nuevas ooportunidades? - Índices de concentración

    def respuesta_providers_concentracion_info(self):
        return "Los índices de concentración miden, en una escala 0-1, la concentración de tus pagos según criterio de proveedores, geográfico, sectorial o temporal. Normalmente, un elevado índicie de concentración representa un mayor riesgo para el negocio"
    
    def respuesta_providers_concentracion_interpretation(self):
        hhi_clients_providers_deviation = float(self.hhi_providers()-self.hhi_providers_sector())/float(self.hhi_providers_sector())
        hhi_geografical_providers_deviation = float(self.hhi_geografical_providers()-self.hhi_geografical_sector_providers())/float(self.hhi_geografical_sector_providers())
        hhi_cnae_providers_deviation = float(self.hhi_cnae_providers()-self.hhi_cnae_sector_providers())/float(self.hhi_cnae_sector_providers())
        hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        hhi_critic_deviation_high = max(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        hhi_critic_deviation_low = min(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        #Solamente interpreto el hhi con desviación más elevada (donde tu como empresa peor estas)
        if hhi_clients_providers_deviation == hhi_critic_deviation_high:
            if hhi_clients_providers_deviation > 0.50:
                return "Tus pagos están muy concentrados en unos pocos proveedores."
            elif hhi_clients_providers_deviation > -0.50:
                return "Tus pagos están razonablemente distribuidos entre tus proveedores."
            else:
                return "Tus pagos están bien diversificados en tus proveedores."
        
        elif hhi_geografical_providers_deviation == hhi_critic_deviation_high:
            if hhi_geografical_providers_deviation > 0.50:
                return "Tus pagos están muy concentrados en una determinada geografía"
            elif hhi_geografical_providers_deviation > -0.50:
                return "Tus pagos están razonablemente distribuidos en distintas geografías."
            else:
                return "Tus pagos están bien diversificados geográficamente."
        
        elif hhi_cnae_providers_deviation == hhi_critic_deviation_high:    
            if hhi_cnae_providers_deviation > 0.50:
                return "Tus pagos están muy concentrados en un determinado sector."
            elif hhi_cnae_providers_deviation > -0.50:
                return "Tus pagos están razonablemente distribuidos en distintos sectores."
            else:
                return "Tus pagos están bien diversificados sectorialmente."
        
        elif hhi_temporal_providers_deviation == hhi_critic_deviation_high:    
            if hhi_temporal_providers_deviation > 0.50:
                return "Tus pagos están muy concentrados en algunas épocas del año"
            elif hhi_temporal_providers_deviation > -0.50:
                return "Tus pagos están razonablemente distribuidos a lo largo del año."
            else:
                return "Tus pagos están bien diversificados a lo largo del año."

    def respuesta_providers_concentracion_hint(self):
        hhi_clients_providers_deviation = float(self.hhi_providers()-self.hhi_providers_sector())/float(self.hhi_providers_sector())
        hhi_geografical_providers_deviation = float(self.hhi_geografical_providers()-self.hhi_geografical_sector_providers())/float(self.hhi_geografical_sector_providers())
        hhi_cnae_providers_deviation = float(self.hhi_cnae_providers()-self.hhi_cnae_sector_providers())/float(self.hhi_cnae_sector_providers())
        hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        hhi_critic_deviation_high = max(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        hhi_critic_deviation_low = min(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        #Solamente interpreto el hhi con desviación más elevada (donde tu como empresa peor estas)
        if hhi_critic_deviation_high > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        elif hhi_critic_deviation_high > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        else:
            return "Sigue así! Mantener índices de concentración bajos mitiga riesgos potenciales para tu negocio. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
    # Ojo,   no se si me convencen las condiciones.....puedes estar con alguna concentración muy baja pero superior a competencia y decirte que estas muy concentrado....

# Como podria hacerlo ? - Margen de venta y/o ratio de eficiencia / ticket medio

    def respuesta_providers_margen_info(self):
        return "El margen comercial (o el ratio de eficiencia) son métricas de calidad de los proveedores y pueden darte una idea de posibles estrategias de precios con tus proveedores."
    
    def respuesta_providers_margen_interpretation(self):
        if len(self.balance_providers_ebitda())>0:
            margen_comercial_providers_deviation = float(self.margen_comercial_providers()-self.margen_comercial_sector_providers())/float(self.margen_comercial_sector_providers())
            if margen_comercial_providers_deviation > 0.50:
                return "Tus proveedores tiene un margen comercial elevado y un buen ratio de eficiencia."
            elif margen_comercial_providers_deviation > -0.50:
                return "Tus proveedores tiene un margen comercial y un ratio de eficiencia razonzables."
            else:
                return "Tus proveedores tiene un margen comercial estrecho y un ratio de eficiencia mejorable."
        else:
            return "No disponemos de tus datos financieros"

    def respuesta_providers_margen_hint(self):
        if len(self.balance_providers_ebitda())>0:
            margen_comercial_providers_deviation = float(self.margen_comercial_providers()-self.margen_comercial_sector_providers())/float(self.margen_comercial_sector_providers())
            if margen_comercial_providers_deviation > 0.50:
                return "Sigue así! Los márgenes elevados de tus proveedores son una métrica de calidad, pero podrías considerar renegociar precios."
            elif margen_comercial_providers_deviation > -0.50:
                return "Bien! Los márgenes de tus proveedores están en línea con el mercado y no pareces tener mucho margen de renegociación de precios."
            else:
                return "Atención! Los márgenes estrechos de tus proveedores pueden indicar una peor calidad y no deberías tener margen de renegociación de precios. Has pensado en buscar otros proveedores? Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones."
        else:
            return "No disponemos de tus datos financieros"

