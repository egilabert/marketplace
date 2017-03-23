#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Recommendations_financial_risk:
###################################################################################################################################################################
# Respuestas risk financiero

    # Ratio de endeudamiento
    def respuesta_finrisk_ratiodeuda_info(self):
        return "El ratio de endeudamiento mide el total de tu deuda sobre el total de tu activo, y te permite valorar tu dependencia de la financiación y la posibilidad de nuevo enduedamiento para posibles inversiones."
    
    def respuesta_finrisk_ratiodeuda_interpretation(self):
        if self.ratio_endeudamiento_sector() > 0:
            ratio_endeudamiento_deviation = float(self.ratio_endeudamiento()-self.ratio_endeudamiento_sector())/float(self.ratio_endeudamiento_sector())
            if ratio_endeudamiento_deviation > 0.20:
                return "Tu ratio de endeudamiento es sensiblemente superior a la media de tu competencia."
            elif ratio_endeudamiento_deviation > -0.20:
                return "Tu ratio de endeudamiento es parecido a la media de tu competencia."
            else:
                return "Tu ratio de endeudamiento es sensiblemente inferior a la media de tu competencia."
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_ratiodeuda_hint(self):
        if self.ratio_endeudamiento_sector() > 0:
            margen_comercial_providers_deviation = float(self.ratio_endeudamiento()-self.ratio_endeudamiento_sector())/float(self.ratio_endeudamiento_sector())
            if margen_comercial_providers_deviation > 0.20:
                return "Atención! Tener altos ratios de endeudamiento puede generar costes financieros elevados o dificultar tu acceso a la financiación. Además, limita tus posibilidades de inversión el corto plazo."
            elif margen_comercial_providers_deviation > -0.20:
                return "Bien! Te recordamos que tu ratio de endeudamiento puede tener efecto en el acceso a nueva financiación para futuras inversiones o necesidades de circulante.."
            else:
                return "Sigue así! Tu bajo ratio de endeudamiento te favorece a la hora de buscar nueva financiación. Tienes nuevos proyectos en la cabeza? Informate sobre nuestros productos de activo."
        else:
            return "No disponemos de los estados financieros de tu competencia"
    ### Falta actualizar el calculo del ratio de endeudamiento....Enric, lo ha calculado?

    # Ratio de deuda sobre EBITDA
    def respuesta_finrisk_deudatotal_info(self):
        return "El ratio deuda / ebitda mide la capacidad de tu negocio de devolver los préstamos actuales. Es una métrica comunmente utilizada para la valoración del riesgo de impago tu empresa, por lo que puede influir en tu acceso a nueva financiación."
    
    def respuesta_finrisk_deudatotal_interpretation(self):
        if self.deuda_total_sector_pond()>0:
            deuda_total_deviation = float(self.deuda_total_pond()-self.deuda_total_sector_pond())/float(self.deuda_total_sector_pond())
            if deuda_total_deviation > 0.50:
                return "Tu ratio de endeudamiento sobre ebitda es sensiblemente superior a la media de tu competencia."
            elif deuda_total_deviation > -0.50:
                return "Tu ratio de endeudamiento  sobre ebitda es parecido a la media de tu competencia."
            else:
                return "Tu ratio de endeudamiento sobre ebitda es sensiblemente inferior a la media de tu competencia."
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_deudatotal_hint(self):
        if self.deuda_total_sector_pond()>0:
            deuda_total_deviation = float(self.deuda_total_pond()-self.deuda_total_sector_pond())/float(self.deuda_total_sector_pond())
            if deuda_total_deviation > 0.50:
                return "Atención! Tener altos ratios de endeudamiento puede generar costes financieros elevados o dificultar tu acceso a la financiación. Además, limita tus posibilidades de inversión el corto plazo.."
            elif deuda_total_deviation > -0.50:
                return "Bien! Te recordamos que tu ratio de endeudamiento puede tener efecto en el acceso a nueva financiación para futuras inversiones o necesidades de circulante."
            else:
                return "Sigue así! Tu bajo ratio de endeudamiento te favorece a la hora de buscar nueva financiación. Crees que es el momento de generar nueva inversión? Informate sobre nuestros productos de activo."
        else:
            return "No disponemos de los estados financieros de tu competencia"
    ### Falta actualizar el calculo del ratio de endeudamiento sobre EBITDA....Enric, lo ha  calculado?

    # Ratio de corto sobre largo
    def respuesta_finrisk_cortolargo_info(self):
        return "El ratio de deuda a corto plazo sobre deuda a largo plazo da una idea del equilibrio de tu estructura financiera, pudiendo significar problemas en el cotro plazo u oportunidades en el largo."
    
    def respuesta_finrisk_cortolargo_interpretation(self):
        if self.id==1610:
            deuda_ebitda = 0.3133
            deuda_largo = 154199.451351351345 * deuda_ebitda * 0.8
            deuda_corto = 154199.451351351345 * deuda_ebitda * 0.2
            ratio_cortolargo = deuda_corto / deuda_largo
            ratio_cortolargo_deviation = float(ratio_cortolargo-self.ratio_sector_corto_largo())/float(self.ratio_sector_corto_largo())
            if ratio_cortolargo_deviation > 0.50:
                return "Tu ratio corto / largo es sensiblemente superior a la media de tu competencia."
            elif ratio_cortolargo_deviation > -0.50:
                return "Tu ratio corto / largo es parecido a la media de tu competencia."
            else:
                return "Tu ratio corto / largo es sensiblemente inferior a la media de tu competencia."
        elif len(self.balance_ebitda())>0:
            ratio_cortolargo_deviation = float(self.ratio_corto_largo()-self.ratio_sector_corto_largo())/float(self.ratio_sector_corto_largo())
            if ratio_cortolargo_deviation > 0.50:
                return "Tu ratio corto / largo es sensiblemente superior a la media de tu competencia."
            elif ratio_cortolargo_deviation > -0.50:
                return "Tu ratio corto / largo es parecido a la media de tu competencia."
            else:
                return "Tu ratio corto / largo es sensiblemente inferior a la media de tu competencia."
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_cortolargo_hint(self):
        if self.id==1610:
            deuda_ebitda = 0.3133
            deuda_largo = 154199.451351351345 * deuda_ebitda * 0.8
            deuda_corto = 154199.451351351345 * deuda_ebitda * 0.2
            ratio_cortolargo = deuda_corto / deuda_largo
            ratio_cortolargo_deviation = float(ratio_cortolargo-self.ratio_sector_corto_largo())/float(self.ratio_sector_corto_largo())
            if ratio_cortolargo_deviation > 0.50:
                return "Atención! Tener altos ratios de endeudamiento puede generar costes financieros elevados o dificultar tu acceso a la financiación circulante. Has pensado en restructurar tu deuda? Si quieres, puedes hablar con tu gestor."
            elif ratio_cortolargo_deviation > -0.50:
                return "Bien! Estás en línea con tu competencia. Si quieres información sobre productos de financiación puedes contactar con tu gestor."
            else:
                return "Sigue así! Tu bajo ratio corto/largo parece indicar que no tienes problemas de liquidez. Sin embargo, si tu ratio de endeudamiento es muy elevado debes tener en cuenta que el acceso a nueva financiación puede verse afectado."
        elif len(self.balance_ebitda())>0:
            ratio_cortolargo_deviation = float(self.ratio_corto_largo()-self.ratio_sector_corto_largo())/float(self.ratio_sector_corto_largo())
            if ratio_cortolargo_deviation > 0.50:
                return "Atención! Tener altos ratios de endeudamiento puede generar costes financieros elevados o dificultar tu acceso a la financiación circulante. Has pensado en restructurar tu deuda? Si quieres, puedes hablar con tu gestor."
            elif ratio_cortolargo_deviation > -0.50:
                return "Bien! Estás en línea con tu competencia. Si quieres información sobre productos de financiación puedes contactar con tu gestor."
            else:
                return "Sigue así! Tu bajo ratio corto/largo parece indicar que no tienes problemas de liquidez. Sin embargo, si tu ratio de endeudamiento es muy elevado debes tener en cuenta que el acceso a nueva financiación puede verse afectado."
        else:
            return "No disponemos de los estados financieros de tu competencia"


    # Coste de financiación
    def respuesta_finrisk_costefin_info(self):
        return "Este ratio te permite valorar tu coste de financiación. Un coste de financiación elevado puede significar una estructura de financiación desequilibrada o reflejar oportunidades para rebajar tus costes financieros."
    
    def respuesta_finrisk_costefin_interpretation(self):
        if len(self.balance_ebitda())>0:
            costes_financiacion_deviation = float(self.costes_financiacion()-self.costes_financiacion_sector())/float(self.costes_financiacion_sector())
            if costes_financiacion_deviation > 0.50:
                return "Tu coste de financiación es sensiblemente superior a la media de tu competencia"
            elif costes_financiacion_deviation > -0.50:
                return "Tu coste de financiación es parecido a la media de tu competencia"
            else:
                return "Tu coste de financiación es sensiblemente inferior a la media de tu competencia"
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_costefin_hint(self):
        if len(self.balance_ebitda())>0:
            costes_financiacion_deviation = float(self.costes_financiacion()-self.costes_financiacion_sector())/float(self.costes_financiacion_sector())
            if costes_financiacion_deviation > 0.50:
                return "Atención! Tus elevados costes de financiación puede reflejar una estructura de financiación inadecuada. Si quieres puedes hablar con tu gestor"
            elif costes_financiacion_deviation > -0.50:
                return "Bien! Tu coste de financiación está en línea con los de tu competencia. ¿Quieres conocer nuestro precios en productos de activo?"
            else:
                return "Sigue así! Tus costes de financiación están muy controlados. Si tus ratios de endeudamiento son también reducidos podrías valorar la posbilidad de invertir en tu crecimiento. En tal caso, conoce nuestros productos de activo aquí"
        else:
            return "No disponemos de los estados financieros de tu competencia"

    # Distribución de deuda por producto.....falta que sea comparable!!
    def respuesta_finrisk_deudaproducto_info(self):
        return "Comparamos tus productos con los de tu competencia para ayudarte a entender la estructura de financiación utilizada por tus comparables."
    

    # Deuda corto sobre ebitda
    def respuesta_finrisk_cortoebitda_info(self):
        return "Este ratio cuantifica la capacidad de tu negocio para repagar la deuda en el corto plazo. Ratios elevados deberían ser una alerta de problemas financieros en el corto plazo."
    
    def respuesta_finrisk_cortoebitda_interpretation(self):
        if self.deuda_corto_sector_pond() > 0:
            ratio_cortoebitda_deviation = float(self.deuda_corto_pond()-self.deuda_corto_sector_pond())/float(self.deuda_corto_sector_pond())
            if ratio_cortoebitda_deviation > 0.50:
                return "Tu ratio de endeudamiento en el corto plazo es sensiblemente superior a la media de tu competencia"
            elif ratio_cortoebitda_deviation > -0.50:
                return "Tu ratio de endeudamiento en el corto plazo es parecido a la media de tu competencia"
            else:
                return "Tu ratio de endeudamiento en el corto plazo es sensiblemente inferior a la media de tu competencia"
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_cortoebitda_hint(self):
        if self.deuda_corto_sector_pond() > 0:
            ratio_cortoebitda_deviation = float(self.deuda_corto_pond()-self.deuda_corto_sector_pond())/float(self.deuda_corto_sector_pond())
            if ratio_cortoebitda_deviation > 0.50:
                return "Atención! Un ratio de endeudamiento a corto plazo tan elevado puede ser una alerta de problemas financieros, y no te permiten tener agilidad y acceso a financiación para cubrir potenciales riesgos de liquidez. Has pensado en restructurar tu deuda? Habla con nosotros..."
            elif ratio_cortoebitda_deviation > -0.50:
                return "Bien! No apreciamos diferencias significativas con la media de tu sector. Si quieres conocer más nuestro productos de circulante clica aquí"
            else:
                return "Sigue así! Tener un ratio de endeudamiento a corto plazo bajo te permite mayor agilidad y acceso a financiación para cubrir potenciales riesgos de liquidez"
        else:
            return "No disponemos de los estados financieros de tu competencia"
    ### Falta actualizar el calculo del ratio de endeudamiento corto sobre EBITDA....Enric, lo ha  calculado?

    # Comentarios con el calendario
    def respuesta_finrisk_calendario_info(self):
        return "Que no te sorprendan los pagos! Utiliza el calendario para controlar y/o anticipar tus pagos, manteniendo un mejor control de tu riesgo de liquidez."
    
    # Días a cobrar / días a pagar
    def respuesta_finrisk_workingcapital_info(self):
        return "Los días a pagar y  a cobrar son un indicador de tus necesidades de working capital. Para mejorarlo, ten en cuenta que disponemos de productos de financiación específicos o que también puedes optimizar tu rotación de existencias."
    
    def respuesta_finrisk_workingcapital_interpretation(self):
        if self.id==1610:
            return "Tus necesidades de working capital son sensiblemente superiores a la media de tu competencia"
        elif self.dias_a_pagar_sector()!=0:
            working_capital_deviation = float(self.dias_a_pagar()-self.dias_a_pagar_sector())/float(self.dias_a_pagar_sector())
            if working_capital_deviation > 0.50:
                return "Tus necesidades de working capital son sensiblemente superiores a la media de tu competencia"
            elif working_capital_deviation > -0.50:
                return "Tus necesidades de working capital son parecidas a la media de tu competencia"
            else:
                return "Tus necesidades de working capital son sensiblemente inferiores a la media de tu competencia"
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_workingcapital_hint(self):
        if self.id==1610:
            return "Atención! Una elevada necesidad de working capital puede generar un problema de tesorería. Has probado a optimizar tus existencias o el cobro a tus clientes? Si quieres estabilizar tu tesorería dispones de nuestros productos de factoring"
        elif self.dias_a_pagar_sector()!=0:
            working_capital_deviation = float(self.dias_a_pagar()-self.dias_a_pagar_sector())/float(self.dias_a_pagar_sector())
            if working_capital_deviation > 0.50:
                return "Atención! Una elevada necesidad de working capital puede generar un problema de tesorería. Has probado a optimizar tus existencias o el cobro a tus clientes? Si quieres estabilizar tu tesorería dispones de nuestros productos de factoring"
            elif working_capital_deviation > -0.50:
                return "Bien! Tus necesidades de working capital estan en línea con tu competencia. Si necesitas financiación circulante, no dudes en conocer nuestros productos."
            else:
                return "Sigue así! Si en algún momento necesitas financiación circulante, no dudes en conocer nuestros productos."
        else:
            return "No disponemos de los estados financieros de tu competencia"
    ### Falta crear una métrica que se llame working capital needs o algo aixi, i que posi en relacio els dias a cobrar vs dias a pagar.

    # Riesgo divisa
    def respuesta_finrisk_divisa_info(self):
        return "Tu exposición a otras divisas incrementan el riesgo al tipo de cambio implícito en el mercado de divisas. Nosotros lo medimos por ti"
    
    def respuesta_finrisk_divisa_interpretation(self):
        if len(self.balance_ebitda())>0:
            riesgo_divisa_deviation = float(self.costes_financiacion()-self.costes_financiacion_sector())/float(self.costes_financiacion_sector())
            if riesgo_divisa_deviation > 0.50:
                return "Tu riesgo de divisa es sensiblemente superior al de tu competencia"
            elif riesgo_divisa_deviation > -0.50:
                return "Tu riesgo de divisa está en línea con el de tu comptencia"
            else:
                return "Tu riesgo de divisa es sensiblemente inferior al de tu comptencia"
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_divisa_hint(self):
        if len(self.balance_ebitda())>0:
            riesgo_divisa_deviation = float(self.costes_financiacion()-self.costes_financiacion_sector())/float(self.costes_financiacion_sector())
            if riesgo_divisa_deviation > 0.50:
                return "Tu negocio está expuesto a variaciones en el mercado de divisas. Si quieres, contrata coberturas con nosotros"
            elif riesgo_divisa_deviation > -0.50:
                return "Tu negocio está expuesto a variaciones en el mercado de divisas. Si quieres, contrata coberturas con nosotros"
            else:
                return "Sigue así! Si en algún momento has pensado en cubrir el riesgo de cambio, conoce nuestros productos especializados"
        else:
            return "No disponemos de los estados financieros de tu competencia"
    ## FALTA CALCULAR METRICA DE RIESGO DIVISA....o no lhe trobat mes avall.


    # Riesgo tipo de interés
    def respuesta_finrisk_interes_info(self):
        return "Tu estructura de financiacíon actual lleva implícito un riesgo al tipo de interés. Nosotros lo medimos por ti"
    
    def respuesta_finrisk_interes_interpretation(self):
        if len(self.balance_ebitda())>0:
            riesgo_interes_deviation = float(self.costes_financiacion()-self.costes_financiacion_sector())/float(self.costes_financiacion_sector())
            if riesgo_interes_deviation > 0.50:
                return "Tu riesgo de tipo de interés es sensiblemente superior al de tu competencia"
            elif riesgo_interes_deviation > -0.50:
                return "Tu riesgo de tipo de interés está en línea con el de tu comptencia"
            else:
                return "Tu riesgo de tipo de interés es sensiblemente inferior al de tu comptencia"
        else:
            return "No disponemos de los estados financieros de tu competencia"

    def respuesta_finrisk_interes_hint(self):
        if len(self.balance_ebitda())>0:
            riesgo_interes_deviation = float(self.costes_financiacion()-self.costes_financiacion_sector())/float(self.costes_financiacion_sector())
            if riesgo_interes_deviation > 0.50:
                return "Tu negocio está expuesto a variaciones en el tipo de interés. Si quieres, contrata coberturas con nosotros"
            elif riesgo_interes_deviation > -0.50:
                return "Tu negocio está expuesto a variaciones en el tipo de interés. Si quieres, contrata coberturas con nosotros"
            else:
                return "Sigue así! Si en algún momento has pensado en cubrir el riesgo de tipod e interés, conoce nuestros productos especializados"
        else:
            return "No disponemos de los estados financieros de tu competencia"
    ## FALTA CALCULAR METRICA DE RIESGO TIPO INTERES...o no lhe trobat mes avall.