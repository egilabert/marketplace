#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recommendations_clients_risk:
# Respuestas risk cliente

    # Riesgo de impago

    # Riesgo de fuga - Fidelización
    def respuesta_riskcliente_fidelizacion_info(self):
        return "La interacción media y años de antigüedad son métricas de fielización: miden la frecuencia con que interactuas con tus clientes a través de las transferencias realizadas y los años transcurridos desde vuestra primera interacción"
    
    def respuesta_riskcliente_fidelizacion_interacciones_interpretation(self):
        if float(self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1].get('c',0)) != 0:
            monthly_sells_deviation = float(self.get_monthly_sells()[len(self.get_monthly_sells())-1].get('c',0)-self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1].get('c',0))/float(self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1].get('c',0))
            if monthly_sells_deviation > 0.20:
                return "En promedio, interactúas más veces con tus clientes que la competencia con los suyos."
            elif monthly_sells_deviation > -0.20:
                return "En promedio, interactúas con tus clientes de manera parecida a tu competencia con los suyos."
            else:
                return "En promedio, interactúas menos veces con tus clientes que la competencia con los suyos."
        else:
            return "No disponemos de los datos de tu comptencia"

    def respuesta_riskcliente_fidelizacion_interacciones_hint(self):
        if self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1].get('c',0) != 0 or self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1].get('c',0) is None:
            monthly_sells_deviation = float(self.get_monthly_sells()[len(self.get_monthly_sells())-1].get('c',0)-self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1].get('c',0))/float(self.get_monthly_sector_avg_sells()[len(self.get_monthly_sector_avg_sells())-1].get('c',0))
            if monthly_sells_deviation > 0.20:
                return "Sigue así! Interactuar a menudo con los clientes es una buena métrica de fidelización, aunque tal vez implique mayor carga administrativa para tu empresa."
            elif monthly_sells_deviation > -0.20:
                return "Bien! No apreciamos diferencias significativas con la media de tu sector."
            else:
                return "Atención! Interactuar poco con los clientes suele aumentar el riesgo de fuga. Parece una buena estrategia realizar acciones de fidelización pero podrías buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "No disponemos de los datos de tu comptencia"
    
    #####FALTAN LAS METRICAS DE ANTIGUEDAD, QUE SON FALSAS 

    # Riesgo de fuga - Frecuencia
    def respuesta_riskcliente_frecuenca_info(self):
        return "El histograma muestra el volumen de compras de tus clientes y los de tu competencia mes a mes, permitiendo identificar fortalezas y/o oportunidades comerciales en distintos momentos del año."
    
    def respuesta_riskcliente_frecuencia_interpretation(self):
        #hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()[len(self.hhi_temporal_clients())-1]['c']-self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])/float(self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])
        hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        if hhi_temporal_clients_deviation > 0.50:
            return "Tus clientes tienen una mayor estacionalidad en su ciclo de compras que los clientes de tu competencia."
        elif hhi_temporal_clients_deviation > -0.50:
            return "Tus clientes tienen una estacionalidad parecida en su ciclo de compras que los clientes de tu competencia."
        else:
            return "Tus clientes tienen una menor estacionalidad en su ciclo de compras que los clientes de tu competencia."

    def respuesta_riskcliente_frecuencia_hint(self):
        #hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()[len(self.hhi_temporal_clients())-1]['c']-self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])/float(self.temp_hhi_temporal_sector_clients()[len(self.temp_hhi_temporal_sector_clients())-1]['c'])
        hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())     
        if hhi_temporal_clients_deviation > 0.50:
            return "Atención! Parece una buena estrategia realizar disminuir el riesgo de estacionalidad implícito en tu cartera de clientes. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        elif hhi_temporal_clients_deviation > -0.50:
            return "Bien! Si quieres reducir el riesgo de estacionalidad implícito en tu cartera de clientes puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "Sigue así! Parece que consigues diversificar tu actividad una buena estrategia realizar disminuir el riesgo de estacionalidad implícito en tu cartera de clientes. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
    #####OJO! No lo pinta por algun error que todavia no se ver...

    # Riesgo de fuga - Penetración
    def respuesta_riskcliente_penetracion_info(self):
        return "El porcentaje de penetración mide el volumen de tu facturación con tus clientes sobre el total de gasto de los clientes; su varianza, indica el cambio respecto al periodo anterior."
    
    def respuesta_riskcliente_penetracion_interpretation(self):
        if len(self.balance_clients_ebitda())>0:
            #my_penetration_client_deviation = float(self.my_penetration_client()[len(self.my_penetration_client())-1]['c']-self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])/float(self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])
            #my_penetration_client_deviation = float(self.my_penetration_client()-self.my_sector_penetration_client())/float(self.my_sector_penetration_client())
            my_penetration_client_deviation = 0.79
            if my_penetration_client_deviation > 0.50:
                return "En promedio, eres un proveedor muy relevante para tus clientes."
            elif my_penetration_client_deviation > -0.50:
                return "En promedio, eres un proveedor relevante para tus clientes."
            else:
                return "En promedio, eres un proveedor poco relevante para tus clientes."
        else:
            return "No disponemos de tus datos financieros"

    def respuesta_riskcliente_penetracion_hint(self):
        if len(self.balance_clients_ebitda())>0:
            #my_penetration_client_deviation = float(self.my_penetration_client()[len(self.my_penetration_client())-1]['c']-self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])/float(self.my_sector_penetration_client()[len(self.my_sector_penetration_client())-1]['c'])
            #my_penetration_client_deviation = float(self.my_penetration_client()-self.my_sector_penetration_client())/float(self.my_sector_penetration_client())
            my_penetration_client_deviation = 0.79
            if my_penetration_client_deviation > 0.50:
                return "Sigue así! Es importante mantener la alta fidelización de tus clientes, pero tienes menos posibilidades de crecer con ellos. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
            elif my_penetration_client_deviation > -0.50:
                return "Bien! Es importante mantener la alta fidelización de tus clientes e intentar crecer con ellos. También puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
            else:
                return "Atención! Deberías tener oportunidades de crecer en tus clientes. También puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones."
        else:
            return "No disponemos de tus datos financieros"
    #####FALTAN LAS VARIACIONES....incluir?

# Riesgo de concentración - Índices de concentración

    def respuesta_riskcliente_concentracion_clientes_hint(self):
        hhi_clients_clients_deviation = float(self.hhi_clients_clients()-self.hhi_clients_sector_clients())/float(self.hhi_clients_sector_clients())
        # hhi_geografical_clients_deviation = float(self.hhi_geografical_clients()-self.hhi_geografical_sector_clients())/float(self.hhi_geografical_sector_clients())
        # hhi_cnae_clients_deviation = float(self.hhi_cnae_clients()-self.hhi_cnae_sector_clients())/float(self.hhi_cnae_sector_clients())
        # hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        # hhi_critic_deviation_high = Max(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        #Solamente interpreto el hhi con desviación más positiva y con desviación más negativa respecto la competencia
        if hhi_clients_clients_deviation > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        elif hhi_clients_clients_deviation > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        else:
            return "Sigue así! Es recomendable mantener unos índices de concentración bajos, pero podrías analizar si tienes oportunidades de crecimiento específicas. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"

    def respuesta_riskcliente_concentracion_geografical_hint(self):
        # hhi_clients_clients_deviation = float(self.hhi_clients_clients()-self.hhi_clients_sector_clients())/float(self.hhi_clients_sector_clients())
        hhi_geografical_clients_deviation = float(self.hhi_geografical_clients()-self.hhi_geografical_sector_clients())/float(self.hhi_geografical_sector_clients())
        # hhi_cnae_clients_deviation = float(self.hhi_cnae_clients()-self.hhi_cnae_sector_clients())/float(self.hhi_cnae_sector_clients())
        # hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        # hhi_critic_deviation_high = Max(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        #Solamente interpreto el hhi con desviación más positiva y con desviación más negativa respecto la competencia
        if hhi_geografical_clients_deviation > 0.20:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        elif hhi_geografical_clients_deviation > -0.20:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        else:
            return "Sigue así! Es recomendable mantener unos índices de concentración bajos, pero podrías analizar si tienes oportunidades de crecimiento específicas. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."

    def respuesta_riskcliente_concentracion_cnae_hint(self):
        # hhi_clients_clients_deviation = float(self.hhi_clients_clients()-self.hhi_clients_sector_clients())/float(self.hhi_clients_sector_clients())
        # hhi_geografical_clients_deviation = float(self.hhi_geografical_clients()-self.hhi_geografical_sector_clients())/float(self.hhi_geografical_sector_clients())
        hhi_cnae_clients_deviation = float(self.hhi_cnae_clients()-self.hhi_cnae_sector_clients())/float(self.hhi_cnae_sector_clients())
        # hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        # hhi_critic_deviation_high = Max(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        #Solamente interpreto el hhi con desviación más positiva y con desviación más negativa respecto la competencia
        if hhi_cnae_clients_deviation > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        elif hhi_cnae_clients_deviation > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        else:
            return "Sigue así! Es recomendable mantener unos índices de concentración bajos, pero podrías analizar si tienes oportunidades de crecimiento específicas. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."

    def respuesta_riskcliente_concentracion_temporal_hint(self):
        # hhi_clients_clients_deviation = float(self.hhi_clients_clients()-self.hhi_clients_sector_clients())/float(self.hhi_clients_sector_clients())
        # hhi_geografical_clients_deviation = float(self.hhi_geografical_clients()-self.hhi_geografical_sector_clients())/float(self.hhi_geografical_sector_clients())
        # hhi_cnae_clients_deviation = float(self.hhi_cnae_clients()-self.hhi_cnae_sector_clients())/float(self.hhi_cnae_sector_clients())
        hhi_temporal_clients_deviation = float(self.hhi_temporal_clients()-self.hhi_temporal_sector_clients())/float(self.hhi_temporal_sector_clients())
        # hhi_critic_deviation_high = Max(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_clients_deviation,hhi_geografical_clients_deviation,hhi_cnae_clients_deviation,hhi_temporal_clients_deviation)
        #Solamente interpreto el hhi con desviación más positiva y con desviación más negativa respecto la competencia
        if hhi_temporal_clients_deviation > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        elif hhi_temporal_clients_deviation > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
        else:
            return "Sigue así! Es recomendable mantener unos índices de concentración bajos, pero podrías analizar si tienes oportunidades de crecimiento específicas. Puedes buscar nuevas oportunidades comerciales utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."

