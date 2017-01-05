#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recommendations_providers_risk:
# Respuestas risk provider
    # Riesgo de iincumplimiento -  hats

    # Riesgo de concentración - Índices de concentración
    def respuesta_riskprovider_concentracion_provider_hint(self):
        hhi_clients_providers_deviation = float(self.hhi_providers()-self.hhi_providers_sector())/float(self.hhi_providers_sector())
        # hhi_geografical_providers_deviation = float(self.hhi_geografical_providers()-self.hhi_geografical_sector_providers())/float(self.hhi_geografical_sector_providers())
        # hhi_cnae_providers_deviation = float(self.hhi_cnae_providers()-self.hhi_cnae_sector_providers())/float(self.hhi_cnae_sector_providers())
        # hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        # hhi_critic_deviation_high = Max(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        #Solamente interpreto el hhi con desviación más elevada (donde tu como empresa peor estas)
        if hhi_clients_providers_deviation > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        elif hhi_clients_providers_deviation > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        else:
            return "Sigue así! Mantener índices de concentración bajos mitiga riesgos potenciales para tu negocio. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
    # Ojo,   no se si me convencen las condiciones.....puedes estar con alguna concentración muy baja pero superior a competencia y decirte que estas muy concentrado....

    def respuesta_riskprovider_concentracion_geografical_hint(self):
        # hhi_clients_providers_deviation = float(self.hhi_providers()-self.hhi_providers_sector())/float(self.hhi_providers_sector())
        hhi_geografical_providers_deviation = float(self.hhi_geografical_providers()-self.hhi_geografical_sector_providers())/float(self.hhi_geografical_sector_providers())
        # hhi_cnae_providers_deviation = float(self.hhi_cnae_providers()-self.hhi_cnae_sector_providers())/float(self.hhi_cnae_sector_providers())
        # hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        # hhi_critic_deviation_high = Max(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        #Solamente interpreto el hhi con desviación más elevada (donde tu como empresa peor estas)
        if hhi_geografical_providers_deviation > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        elif hhi_geografical_providers_deviation > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        else:
            return "Sigue así! Mantener índices de concentración bajos mitiga riesgos potenciales para tu negocio. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
    
    def respuesta_riskprovider_concentracion_cnae_hint(self):
        # hhi_clients_providers_deviation = float(self.hhi_providers()-self.hhi_providers_sector())/float(self.hhi_providers_sector())
        # hhi_geografical_providers_deviation = float(self.hhi_geografical_providers()-self.hhi_geografical_sector_providers())/float(self.hhi_geografical_sector_providers())
        hhi_cnae_providers_deviation = float(self.hhi_cnae_providers()-self.hhi_cnae_sector_providers())/float(self.hhi_cnae_sector_providers())
        # hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        # hhi_critic_deviation_high = Max(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        #Solamente interpreto el hhi con desviación más elevada (donde tu como empresa peor estas)
        if hhi_cnae_providers_deviation > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        elif hhi_cnae_providers_deviation > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        else:
            return "Sigue así! Mantener índices de concentración bajos mitiga riesgos potenciales para tu negocio. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
    
    def respuesta_riskprovider_concentracion_temporal_hint(self):
        # hhi_clients_providers_deviation = float(self.hhi_providers()-self.hhi_providers_sector())/float(self.hhi_providers_sector())
        # hhi_geografical_providers_deviation = float(self.hhi_geografical_providers()-self.hhi_geografical_sector_providers())/float(self.hhi_geografical_sector_providers())
        # hhi_cnae_providers_deviation = float(self.hhi_cnae_providers()-self.hhi_cnae_sector_providers())/float(self.hhi_cnae_sector_providers())
        hhi_temporal_providers_deviation = float(self.hhi_temporal_providers()-self.hhi_temporal_sector_providers())/float(self.hhi_temporal_sector_providers())
        # hhi_critic_deviation_high = Max(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        # hhi_critic_deviation_low = Min(hhi_clients_providers_deviation,hhi_geografical_providers_deviation,hhi_cnae_providers_deviation,hhi_temporal_providers_deviation)
        #Solamente interpreto el hhi con desviación más elevada (donde tu como empresa peor estas)
        if hhi_temporal_providers_deviation > 0.50:
            return "Atención! Un alto índice de concentración puede suponer riesgos para tu empresa. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        elif hhi_temporal_providers_deviation > -0.50:
            return "Bien! Es recomendable mantener unos índices de concentración razonables. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación"
        else:
            return "Sigue así! Mantener índices de concentración bajos mitiga riesgos potenciales para tu negocio. Puedes buscar nuevos proveedores utilizando nuestro motor de recomendaciones, filtrando por tus prioridades de diversificación."
    