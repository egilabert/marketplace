#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from empresas.models import Empresa
from .models import Rating
from .forms import RatingForm
import random
from .permissions import *
import json
from django.core.serializers.json import DjangoJSONEncoder

"""-------------------------------------------------------"""
"""				EMPRESAS VIEWS 							  """
"""-------------------------------------------------------"""
BANCO_PRESENTACION = 1

@login_required
def SearchView(request):
	if has_roborisk_permission(request.user) or request.user.is_superuser:
		if request.user.is_staff or request.user.is_superuser:
			autofilter = dict()
			company = Empresa.objects.all()
			request.session['banco'] = BANCO_PRESENTACION
			request.session['journey'] = False
			request.session['summary'] = True
			request.session.modified = True
			for c in company:
				autofilter[c.name] = c.image

			context = {
				'autofilter': json.dumps(autofilter, cls=DjangoJSONEncoder),
				'buttons': False
			}
			return render(request, "risk_cro/search.html", context)
		else:
			try:
				del request.session['company']
				del request.session['recommended_clients_page']
				del request.session['summary']
				del request.session['banco']
			except:
				pass
			company_id = 990
			request.session['banco'] = BANCO_PRESENTACION
			request.session['company'] = company_id
			request.session['summary'] = True
			request.session.modified = True
			company = Empresa.objects.filter(pk=company_id)
			company = company.prefetch_related('estados_financieros','transfers')[0]
			return redirect("risk_cro/summary", {'empresa': company, 'company': company})
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/cro/", {})
		
def HomeView(request):
	return render(request, "cro_home.html", {'menu': False})

def CreditRaterView(request):
	form = RatingForm()
	context = {
		'menu': False,
		'power_but_black': True,
		'form': form
	}
	return render(request, "credit_risk.html", context)

def RaterView(request):
	# if this is a POST request we need to process the form data

	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RatingForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			rater = Rating()
			# process the data in form.cleaned_data as required
			rater.name = form.cleaned_data['name']
			rater.sector = form.cleaned_data['sector']
			rater.antiguedad = form.cleaned_data['antiguedad']
			rater.fondos_propios = form.cleaned_data['fondos_propios']
			rater.activo_corriente = form.cleaned_data['activo_corriente']
			rater.activo_no_corriente = form.cleaned_data['activo_no_corriente']
			rater.pasivo_corriente = form.cleaned_data['pasivo_corriente']
			rater.pasivo_no_corriente = form.cleaned_data['pasivo_no_corriente']
			rater.importe_neto_cifra_negocio = form.cleaned_data['importe_neto_cifra_negocio']
			rater.gastos_financieros = form.cleaned_data['gastos_financieros']
			rater.resultados_antes_impuestos = form.cleaned_data['resultados_antes_impuestos']
			rater.save()

			# Calculo de los ratios financieros
			nombres = {}
			nombres['ratio_solvencia'] = "Ratio de solvencia"
			nombres['ratio_endeudamiento'] = "Ratio de endeudamiento"
			nombres['ratio_endeudamiento_cp'] = "Ratio de endeudamiento corto plazo"
			nombres['ratio_autonomia'] = "Ratio de autonomia"
			nombres['ratio_cobertura_inmovilizado_FFPP'] = "Ratio de cobertura inmovilizado FFPP"
			nombres['ratio_rentabilidad_economica'] = "Ratio de rentabilidad economica"
			nombres['ratio_autonomia_financiera'] = "Ratio de autonomia financiera"
			nombres['ratio_dependencia_financiera'] = "Ratio de dependencia financiera"
			nombres['ratio_gastos_financieros'] = "Ratio de gastos financieros"
			nombres['ratio_rentabilidad_financiera'] = "Ratio de rentabilidad financiera"
			nombres['ratio_rentabilidad_inversion'] = "Ratio de rentabilidad inversion"
			nombres['ratio_resultados_sobre_ventas'] = "Ratio de resultados sobre ventas"

			# Calculo de los ratios financieros
			ratios = {}
			ratio_solvencia = rater.ratio_solvencia()
			ratio_endeudamiento = rater.ratio_endeudamiento()
			ratio_endeudamiento_cp = rater.ratio_endeudamiento_cp()
			ratio_autonomia = rater.ratio_autonomia()
			ratio_cobertura_inmovilizado_FFPP = rater.ratio_cobertura_inmovilizado_FFPP()
			ratio_rentabilidad_economica = rater.ratio_rentabilidad_economica()
			ratio_autonomia_financiera = rater.ratio_autonomia_financiera()
			ratio_dependencia_financiera = rater.ratio_dependencia_financiera()
			ratio_gastos_financieros = rater.ratio_gastos_financieros()
			ratio_rentabilidad_financiera = rater.ratio_rentabilidad_financiera()
			ratio_rentabilidad_inversion = rater.ratio_rentabilidad_inversion()
			ratio_resultados_sobre_ventas = rater.ratio_resultados_sobre_ventas()
			datos_sectorial = rater.sectorial_data[rater.sectorial_data['COD_SEC20'].isin(rater.get_sector_params(rater.sector)['#'].values)]

			# Calculo de los tramos del sector de los ratios financieros
			tramos = {}
			tramo_ratio_solvencia = 12.5+(25*(rater.get_tramo(rater.ratio_solvencia(), datos_sectorial, 'R_Solvencia')-1))
			tramo_ratio_endeudamiento = 12.5+(25*(rater.get_tramo(rater.ratio_endeudamiento(), datos_sectorial, 'R_Endeudamiento')-1))
			tramo_ratio_endeudamiento_cp = 12.5+(25*(rater.get_tramo(rater.ratio_endeudamiento_cp(), datos_sectorial, 'R_Endeudamiento_CP')-1))
			tramo_ratio_autonomia = 12.5+(25*(rater.get_tramo(rater.ratio_autonomia(), datos_sectorial, 'R_Autonomia')-1))
			tramo_ratio_cobertura_inmovilizado_FFPP = 12.5+(25*(rater.get_tramo(rater.ratio_cobertura_inmovilizado_FFPP(), datos_sectorial, 'R_Cobertura_Inmovilizado_FFPP')-1))
			tramo_ratio_rentabilidad_economica = 12.5+(25*(rater.get_tramo(rater.ratio_rentabilidad_economica(), datos_sectorial, 'R_Rentabilidad_Economica')-1))
			tramo_ratio_autonomia_financiera = 12.5+(25*(rater.get_tramo(rater.ratio_autonomia_financiera(), datos_sectorial, 'R_Autonomia_Financiera')-1))
			tramo_ratio_dependencia_financiera = 12.5+(25*(rater.get_tramo(rater.ratio_dependencia_financiera(), datos_sectorial, 'R_Dependencia_Financiera')-1))
			tramo_ratio_gastos_financieros = 12.5+(25*(rater.get_tramo(rater.ratio_gastos_financieros(), datos_sectorial, 'R_Gastos_Financieros')-1))
			tramo_ratio_rentabilidad_financiera = 12.5+(25*(rater.get_tramo(rater.ratio_rentabilidad_financiera(), datos_sectorial, 'R_Rentabilidad_Financiera')-1))
			tramo_ratio_rentabilidad_inversion = 12.5+(25*(rater.get_tramo(rater.ratio_rentabilidad_inversion(), datos_sectorial, 'R_Rentabilidad_Inversion')-1))
			tramo_ratio_resultados_sobre_ventas = 12.5+(25*(rater.get_tramo(rater.ratio_resultados_sobre_ventas(), datos_sectorial, 'R_Resultados_Sobre_Ventas')-1))
			context = {
				'nombres': nombres,
				'tramo_ratio_solvencia': tramo_ratio_solvencia,
				'tramo_ratio_endeudamiento': tramo_ratio_endeudamiento,
				'tramo_ratio_endeudamiento_cp': tramo_ratio_endeudamiento_cp,
				'tramo_ratio_autonomia': tramo_ratio_autonomia,
				'tramo_ratio_cobertura_inmovilizado_FFPP': tramo_ratio_cobertura_inmovilizado_FFPP,
				'tramo_ratio_rentabilidad_economica': tramo_ratio_rentabilidad_economica,
				'tramo_ratio_autonomia_financiera': tramo_ratio_autonomia_financiera,
				'tramo_ratio_dependencia_financiera': tramo_ratio_dependencia_financiera,
				'tramo_ratio_gastos_financieros': tramo_ratio_gastos_financieros,
				'tramo_ratio_rentabilidad_financiera': tramo_ratio_rentabilidad_financiera,
				'tramo_ratio_rentabilidad_inversion': tramo_ratio_rentabilidad_inversion,
				'tramo_ratio_resultados_sobre_ventas': tramo_ratio_resultados_sobre_ventas,
				
				'ratio_solvencia': ratio_solvencia*100,
				'ratio_endeudamiento': ratio_endeudamiento*100,
				'ratio_endeudamiento_cp': ratio_endeudamiento_cp*100,
				'ratio_autonomia': ratio_autonomia*100,
				'ratio_cobertura_inmovilizado_FFPP': ratio_cobertura_inmovilizado_FFPP*100,
				'ratio_rentabilidad_economica': ratio_rentabilidad_economica*100,
				'ratio_autonomia_financiera': ratio_autonomia_financiera*100,
				'ratio_dependencia_financiera': ratio_dependencia_financiera*100,
				'ratio_gastos_financieros': ratio_gastos_financieros*100,
				'ratio_rentabilidad_financiera': ratio_rentabilidad_financiera*100,
				'ratio_rentabilidad_inversion': ratio_rentabilidad_inversion*100,
				'ratio_resultados_sobre_ventas': ratio_resultados_sobre_ventas*100,
				'ratios': ratios,
				'r_tramos': tramos,
				'rate': rater,
				'rating': rater.rate_it()[0],
				'rating_text': rater.rate_it()[1],
				'tramos': rater.tramos,
				'tramos_grafico': rater.tramos_grafico
			}
			# redirect to a new URL:
			return render(request, "informe.html", context)
		else:
			return render(request, "errors.html", {'form': form})

	# if a GET (or any other method) we'll create a blank form
	else:
		return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required
def SummaryView(request):
	if has_roborisk_permission(request.user) or request.user.is_superuser:
		try:
			referrer = request.META['HTTP_REFERER']
			if request.GET and request.GET.get('company_name',None):
				name = request.GET['company_name']
				try:
					del request.session['company']
					del request.session['recommended_clients_page']
				except:
					pass
				try:
					got_it = Empresa.objects.filter(name=name).first()
					company = got_it.pk #1492 #randint(0, queryset.count() - 1) # # ## 865 865-1
				except:
					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
				request.session['company'] = company
				request.session['summary'] = True
				request.session.modified = True
				company_id = request.session.get('company')
				company = Empresa.objects.filter(pk=company_id)
				company = company.prefetch_related('estados_financieros','transfers')[0]
				return render(request, "risk_cro/summary.html", {'empresa': company, 'company': company})
			else:
				company_id = request.session.get('company')
				company = Empresa.objects.filter(pk=company_id)
				company = company.prefetch_related('estados_financieros','transfers')[0]
				return render(request, "risk_cro/summary.html", {'empresa': company, 'company': company})
		except:
			company_id = request.session.get('company')
			company = Empresa.objects.filter(pk=company_id)
			company = company.prefetch_related('estados_financieros','transfers')[0]
			return render(request, "risk_cro/summary.html", {'empresa': company, 'company': company})
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/cro/", {})


@login_required
def EmpresaDetailView(request, pk=None):
	if has_roborisk_permission(request.user) or request.user.is_superuser:
		try:
			referrer = request.META['HTTP_REFERER']
			if int(pk) == int(request.session.get('company')):
				key = 'self'
			elif 'clients' in referrer:
				key = 'client'
			elif 'providers' in referrer:	
				key = 'provider'
			else:
				key = 'none'
		except:
			key = 'none'

		empresa = Empresa.objects.filter(pk=pk)
		company_id = request.session.get('company')
		company = Empresa.objects.filter(pk=company_id)[0]
		empresa = empresa.prefetch_related('estados_financieros','transfers')[0]

		ventas = []
		fechas = []
		ebitda = []
		depreciaciones = []
		resultado_explotacion = []
		amortizaciones = []
		sells_sector = []
		sells_me = []
		ebitda_sector = []
		ebitda_me = []
		resultados_sector = []
		resultados_me = []
		# try:
		num_proveedores = empresa.get_providers().count()
		hhi_providers = empresa.hhi_providers()
		for i, estado in enumerate(empresa.estados_financieros.all()):
			if i == 0:
				fechas.append(estado.ejercicio)
				depreciaciones.append(estado.depreciaciones)
				ebitda.append(estado.ebitda)
				resultado_explotacion.append(estado.resultado_explotacion)
				ventas.append(estado.ventas)
				amortizaciones.append(estado.amortizaciones)
				sells_me.append({'ejercicio': estado.ejercicio, 'c': ventas[len(ventas)-1]})
				ebitda_me.append({'ejercicio': estado.ejercicio, 'c': ebitda[len(ebitda)-1]})
				resultados_me.append({'ejercicio': estado.ejercicio, 'c': resultado_explotacion[len(resultado_explotacion)-1]})
			if int(company_id)==int(pk) and int(company_id)==990 and (i != 0):
				print(fechas)
				fechas.append(estado.ejercicio)
				depreciaciones.append(depreciaciones[i-1]*random.uniform(1, 1.1))
				ebitda.append(ebitda[i-1]*random.uniform(1, 1.1))
				resultado_explotacion.append(resultado_explotacion[i-1]*random.uniform(1, 1.1))
				ventas.append(ventas[i-1]*random.uniform(1, 1.1))
				amortizaciones.append(amortizaciones[i-1]*random.uniform(1, 1.1))
				num_proveedores = empresa.get_providers().count()
				hhi_providers = empresa.hhi_providers()
				margen_comercial_sector_clientes = 0.16
				sells_me.append({'ejercicio': estado.ejercicio, 'c': ventas[len(ventas)-1]})
				ebitda_me.append({'ejercicio': estado.ejercicio, 'c': ebitda[len(ebitda)-1]})
				resultados_me.append({'ejercicio': estado.ejercicio, 'c': resultado_explotacion[len(resultado_explotacion)-1]})
			if int(company_id)==int(pk) and int(company_id)==1610 and (i != 0):
				fechas.append(estado.ejercicio)
				depreciaciones.append(depreciaciones[i-1]*random.uniform(1, 1.1))
				ebitda.append(ebitda[i-1]*random.uniform(0.93, 1.001))
				resultado_explotacion.append(resultado_explotacion[i-1]*random.uniform(0.93, 1.001))
				ventas.append(ventas[i-1]*random.uniform(0.99, 1.05))
				amortizaciones.append(amortizaciones[i-1]*random.uniform(1, 1.1))
				num_proveedores = empresa.get_providers().count()
				hhi_providers = empresa.hhi_providers()
				margen_comercial_sector_clientes = empresa.margen_comercial_sector_clientes()
				sells_me.append({'ejercicio': estado.ejercicio, 'c': ventas[len(ventas)-1]})
				ebitda_me.append({'ejercicio': estado.ejercicio, 'c': ebitda[len(ebitda)-1]})
				resultados_me.append({'ejercicio': estado.ejercicio, 'c': resultado_explotacion[len(resultado_explotacion)-1]})
			elif i!=0 and int(company_id)!=1610 and int(company_id)!=990:
				fechas.append(estado.ejercicio)
				depreciaciones.append(estado.depreciaciones)
				ebitda.append(estado.ebitda)
				resultado_explotacion.append(estado.resultado_explotacion)
				ventas.append(estado.ventas)
				amortizaciones.append(estado.amortizaciones)
				margen_comercial_sector_clientes = empresa.margen_comercial_sector_clientes()
				sells_me = list(empresa.balance_sells())
				ebitda_me = list(empresa.balance_ebitda())
				resultados_me = list(empresa.resultado_explotacion())
		# except:
		# 	ventas.append(0)
		# 	depreciaciones.append(0)
		# 	ebitda.append(0)
		# 	resultado_explotacion.append(0)
		# 	amortizaciones.append(0)
		# 	num_proveedores = empresa.get_providers().count()
		# 	hhi_providers = empresa.hhi_providers()
		# 	margen_comercial_sector_clientes = empresa.margen_comercial_sector_clientes()

		resultados_sector = list(empresa.resultado_explotacion_avg_sector())
		ebitda_sector = list(empresa.balance_ebitda_avg_sector())
		sells_sector = list(empresa.balance_sells_avg_sector())

		if not fechas:
			fechas.append(0)
		if not ventas:
			ventas.append(0)
		if not depreciaciones:
			depreciaciones.append(0)
		if not ebitda:
			ebitda.append(0)
		if not resultado_explotacion:
			resultado_explotacion.append(0)
		if not amortizaciones:
			amortizaciones.append(0)

		buys_amount = json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder)
		buys_count = json.dumps(list(empresa.get_monthly_buys()), cls=DjangoJSONEncoder)
		sells_amount = json.dumps(list(empresa.get_monthly_sells_amount()), cls=DjangoJSONEncoder)
		sells_count = json.dumps(list(empresa.get_monthly_sells()), cls=DjangoJSONEncoder)
		titulo = 'Ventas mensuales'

		if len(ventas)>1:
			delta_ventas = (ventas[len(ventas)-1] - ventas[len(ventas)-2])/ventas[len(ventas)-2]
		else:
			delta_ventas = 0
		if len(ebitda)>1:
			delta_ebitda = (ebitda[len(ebitda)-1] - ebitda[len(ebitda)-2])/ebitda[len(ebitda)-2]
			trabajadores = int(ebitda[len(ebitda)-1]/1200)
		else:
			trabajadores = 10
			delta_ebitda = 0
		if len(resultado_explotacion)>1:
			delta_resultados_explotacion = (resultado_explotacion[len(resultado_explotacion)-1] - resultado_explotacion[len(resultado_explotacion)-2])/resultado_explotacion[len(resultado_explotacion)-2]
		else:
			delta_resultados_explotacion = 0

		context = {
			'referrer': key,
			'delta_ventas': delta_ventas,
			'trabajadores': trabajadores,
			'delta_ebitda': delta_ebitda,
			'delta_resultados_explotacion': delta_resultados_explotacion,
			'company': company,
			'empresa':empresa,
			'titulo': titulo,
			'num_proveedores': num_proveedores,
			'hhi_providers': hhi_providers,
			'last_ventas': ventas[len(ventas)-1],
			'last_ebitda': ebitda[len(ebitda)-1],
			'last_fechas': fechas[len(fechas)-1],
			'ventas': json.dumps(ventas),
			'ebitda': json.dumps(ebitda),
			'depreciaciones': json.dumps(depreciaciones),
			'clients_by_sector': json.dumps(list(empresa.clients_by_sector()), cls=DjangoJSONEncoder),
			'clients_sector_by_sector': json.dumps(list(empresa.clients_sector_by_sector()), cls=DjangoJSONEncoder),
			'clients_by_region': json.dumps(list(empresa.clients_by_region()), cls=DjangoJSONEncoder),
			'clients_sector_by_region': json.dumps(list(empresa.clients_sector_by_region()), cls=DjangoJSONEncoder),
			'buys_amount': buys_amount,
			'buys_count': buys_count,
			'sells_amount': sells_amount,
			'sells_count': sells_count,
			'amortizaciones': json.dumps(amortizaciones),
			'resultado_explotacion': json.dumps(resultado_explotacion),
			'fechas': json.dumps(fechas),
			'get_monthly_buys_amount': json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder),
			'get_sector_total_monthly_buys_amount': json.dumps(list(empresa.get_sector_total_monthly_buys_amount()), cls=DjangoJSONEncoder),
			'balance_sells_avg_sector': json.dumps(sells_sector, cls=DjangoJSONEncoder),
			'balance_sells': json.dumps(sells_me, cls=DjangoJSONEncoder),
			'balance_ebitda_avg_sector': json.dumps(ebitda_sector, cls=DjangoJSONEncoder),
			'balance_ebitda': json.dumps(ebitda_me, cls=DjangoJSONEncoder),
			'balance_resultado_avg_sector': json.dumps(resultados_sector, cls=DjangoJSONEncoder),
			'balance_resultado': json.dumps(resultados_me, cls=DjangoJSONEncoder),
			'journey': request.session.get('journey'),
			'summary': request.session.get('summary'),
			'banco': request.session.get('banco')
			}

		return render(request, 'risk_cro/company_detail.html', context)
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/cro/", {})

@login_required
def MarketRiskRecommendationsView(request):
	if has_roborisk_permission(request.user) or request.user.is_superuser:
		company_id = request.session.get('company')
		company = Empresa.objects.filter(pk=company_id)
		company = company.prefetch_related('estados_financieros','cirbe','productos')[0]
		try:
			ultimos_eeff = company.estados_financieros.reverse()[0]
		except:
			ultimos_eeff = Empresa()

		if int(company_id)==990:
			penetracion = 0.79
		else:
			penetracion = company.my_penetration_client()

		ventas = []
		fechas = []
		ebitda = []
		ebit = []
		depreciaciones = []
		resultado_explotacion = []
		amortizaciones = []
		sells_sector = []
		sells_me = []
		ebit_me = []
		ebitda_sector = []
		ebitda_me = []
		resultados_sector = []
		resultados_me = []
		num_proveedores = company.get_providers().count()
		hhi_providers = company.hhi_providers()
		for i, estado in enumerate(company.estados_financieros.all()):
			if i == 0:
				fechas.append(estado.ejercicio)
				depreciaciones.append(estado.depreciaciones)
				ebitda.append(estado.ebitda)
				resultado_explotacion.append(estado.resultado_explotacion)
				ventas.append(estado.ventas)
				amortizaciones.append(estado.amortizaciones)
				ebit.append(estado.ebitda + estado.amortizaciones + estado.depreciaciones)
				sells_me.append({'ejercicio': estado.ejercicio, 'c': ventas[len(ventas)-1]})
				ebitda_me.append({'ejercicio': estado.ejercicio, 'c': ebitda[len(ebitda)-1]})
				ebit_me.append({'ejercicio': estado.ejercicio, 'c': ebit[len(ebit)-1]})
				resultados_me.append({'ejercicio': estado.ejercicio, 'c': resultado_explotacion[len(resultado_explotacion)-1]})
			if int(company_id)==990 and (i != 0):
				fechas.append(estado.ejercicio)
				depreciaciones.append(depreciaciones[i-1]*random.uniform(1, 1.1))
				ebitda.append(ebitda[i-1]*random.uniform(1, 1.1))
				ebit.append(ebitda[i] + estado.amortizaciones + estado.depreciaciones)
				resultado_explotacion.append(resultado_explotacion[i-1]*random.uniform(1, 1.1))
				ventas.append(ventas[i-1]*random.uniform(1, 1.1))
				amortizaciones.append(amortizaciones[i-1]*random.uniform(1, 1.1))
				num_proveedores = company.get_providers().count()
				hhi_providers = company.hhi_providers()
				margen_comercial_sector_clientes = 0.16
				sells_me.append({'ejercicio': estado.ejercicio, 'c': ventas[len(ventas)-1]})
				ebitda_me.append({'ejercicio': estado.ejercicio, 'c': ebitda[len(ebitda)-1]})
				ebit_me.append({'ejercicio': estado.ejercicio, 'c': ebit[len(ebit)-1]})
				resultados_me.append({'ejercicio': estado.ejercicio, 'c': resultado_explotacion[len(resultado_explotacion)-1]})
			if int(company_id)==1610 and (i != 0):
				fechas.append(estado.ejercicio)
				depreciaciones.append(depreciaciones[i-1]*random.uniform(1, 1.1))
				ebitda.append(ebitda[i-1]*random.uniform(0.93, 1.001))
				ebit.append(ebitda[i]*random.uniform(0.93, 1.001) + estado.amortizaciones + estado.depreciaciones)
				resultado_explotacion.append(resultado_explotacion[i-1]*random.uniform(0.93, 1.001))
				ventas.append(ventas[i-1]*random.uniform(0.99, 1.05))
				amortizaciones.append(amortizaciones[i-1]*random.uniform(1, 1.1))
				num_proveedores = company.get_providers().count()
				hhi_providers = company.hhi_providers()
				margen_comercial_sector_clientes = company.margen_comercial_sector_clientes()
				sells_me.append({'ejercicio': estado.ejercicio, 'c': ventas[len(ventas)-1]})
				ebitda_me.append({'ejercicio': estado.ejercicio, 'c': ebitda[len(ebitda)-1]})
				ebit_me.append({'ejercicio': estado.ejercicio, 'c': ebit[len(ebit)-1]})
				resultados_me.append({'ejercicio': estado.ejercicio, 'c': resultado_explotacion[len(resultado_explotacion)-1]})
			elif i!=0 and int(company_id)!=1610 and int(company_id)!=990:
				fechas.append(estado.ejercicio)
				depreciaciones.append(estado.depreciaciones)
				ebitda.append(estado.ebitda)
				resultado_explotacion.append(estado.resultado_explotacion)
				ventas.append(estado.ventas)
				amortizaciones.append(estado.amortizaciones)
				margen_comercial_sector_clientes = company.margen_comercial_sector_clientes()
				sells_me = list(company.balance_sells())
				ebitda_me = list(company.balance_ebitda())
				resultados_me = list(company.resultado_explotacion())

		if not fechas:
			fechas.append(0)
		if not ventas:
			ventas.append(0)
		if not depreciaciones:
			depreciaciones.append(0)
		if not ebitda:
			ebitda.append(0)
		if not resultado_explotacion:
			resultado_explotacion.append(0)
		if not amortizaciones:
			amortizaciones.append(0)

		if len(sells_me)>1:
			delta_ventas = (sells_me[len(sells_me)-1]['c'] - sells_me[len(sells_me)-2]['c'])/sells_me[len(sells_me)-2]['c']
		if len(ebitda_me)>1:
			delta_ebitda = (ebitda_me[len(ebitda_me)-1]['c'] - ebitda_me[len(ebitda_me)-2]['c'])/ebitda_me[len(ebitda_me)-2]['c']
		if len(resultados_me)>1:
			delta_resultados_explotacion = (resultados_me[len(resultados_me)-1]['c'] - resultados_me[len(resultados_me)-2]['c'])/resultados_me[len(resultados_me)-2]['c']

		context = {
			'company':company,
			'penetracion': penetracion,
			'riesgo_impago_clientes': json.dumps(list(company.riesgo_impago_clientes()), cls=DjangoJSONEncoder),
			'riesgo_impago_clientes_sector': json.dumps(list(company.riesgo_impago_clientes_sector()), cls=DjangoJSONEncoder),
			'get_monthly_buys': json.dumps(list(company.get_monthly_buys_amount()), cls=DjangoJSONEncoder),
			'get_monthly_sector_avg_buys': json.dumps(list(company.get_sector_total_monthly_buys_amount()), cls=DjangoJSONEncoder),
			'productos_variable': company.productos_con_tipo_variable().all(),
			'ultimos_eeff': ultimos_eeff,
			'PIB_espana': 3.2,
			'PIB_sector': 2.4,
			'PIB_comparables': 2.6,
			'journey': request.session.get('journey'),
			'balance_providers_sells_avg_sector': json.dumps(list(company.balance_providers_sells_avg_sector()), cls=DjangoJSONEncoder),
			'balance_sells_avg_sector': json.dumps(list(company.balance_sells_avg_sector()), cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_sells_avg_sector()), cls=DjangoJSONEncoder),
			'balance_sells': json.dumps(sells_me, cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_sells()), cls=DjangoJSONEncoder),
			'balance_ebitda_avg_sector': json.dumps(list(company.balance_ebitda_avg_sector()), cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_ebitda_avg_sector()), cls=DjangoJSONEncoder),
			'balance_ebitda': json.dumps(ebitda_me, cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_ebitda()), cls=DjangoJSONEncoder),
			'balance_ebit_avg_sector': json.dumps(list(company.balance_ebit_avg_sector()), cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_ebit_avg_sector()), cls=DjangoJSONEncoder),
			'balance_ebit': json.dumps(list(ebit_me), cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_ebit()), cls=DjangoJSONEncoder),
			'balance_resultados_avg_sector': json.dumps(list(company.resultado_explotacion_avg_sector()), cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_resultados_avg_sector()), cls=DjangoJSONEncoder),
			'balance_resultados': json.dumps(list(resultados_me), cls=DjangoJSONEncoder), #json.dumps(list(company.balance_clients_ebit()), cls=DjangoJSONEncoder),
			'banco': request.session.get('banco')
			}
		return render(request, 'risk_cro/risk_market.html', context)
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/cro/", {})

@login_required
def CommercialClientsRecommendationsView(request):
	if has_roborisk_permission(request.user) or request.user.is_superuser:
		try:
			referrer = request.META['HTTP_REFERER']
			if 'intro' in referrer:
				request.session['journey'] = False
		except:
			request.session['journey'] = False

		company_id = request.session.get('company')
		empresa = Empresa.objects.filter(pk=company_id)
		empresa = empresa.prefetch_related(None)
		empresa = empresa.prefetch_related('transfers', 'destination_reference', 'destination_reference__origin_reference')[0]

		if int(company_id) == 990:
			sells_sector = [{u'ejercicio': u'2011', 'c': 546283.4647849461}, {u'ejercicio': u'2012', 'c': 456645.75040462404}, {u'ejercicio': u'2013', 'c': 378471.62807453406}, {u'ejercicio': u'2014', 'c': 456921.41805970157}]
			sells_me = [{u'ejercicio': u'2011', 'c': 592696.61117647061}, {u'ejercicio': u'2012', 'c': 534303.62062499998}, {u'ejercicio': u'2013', 'c': 399953.46552631578}, {u'ejercicio': u'2014', 'c': 491070.38647058822}]
			ebitda_sector = [{u'ejercicio': u'2011', 'c': 49361.97748407643}, {u'ejercicio': u'2012', 'c': 47984.25817891373}, {u'ejercicio': u'2013', 'c': 46471.11822525595}, {u'ejercicio': u'2014', 'c': 54865.1086259542}]
			ebitda_me = [{u'ejercicio': u'2011', 'c': 51794.07494505495}, {u'ejercicio': u'2012', 'c': 45185.49206521739}, {u'ejercicio': u'2013', 'c': 41847.803749999985}, {u'ejercicio': u'2014', 'c': 54199.451351351345}]
			resultados_sector = [{u'ejercicio': u'2011', 'c': 66543.67525477704}, {u'ejercicio': u'2012', 'c': 53854.49316293933}, {u'ejercicio': u'2013', 'c': 16644.12122866895}, {u'ejercicio': u'2014', 'c': 76736.3875572519}]
			resultados_me = [{u'ejercicio': u'2011', 'c': 63690.474505494498}, {u'ejercicio': u'2012', 'c': 42998.05847826087}, {u'ejercicio': u'2013', 'c': 10357.194875000005}, {u'ejercicio': u'2014', 'c': 82367.53648648648}]
			penetration = 0.79
			margen_comercial_sector_clientes = 0.17
			average_transfer_from_client = empresa.average_transfer_from_client()
			respuesta_clientes_ventas_interpretation = empresa.respuesta_clientes_ventas_interpretation()
			respuesta_clientes_ventas_hint = empresa.respuesta_clientes_ventas_hint()
			respuesta_clientes_ebitda_interpretation = empresa.respuesta_clientes_ebitda_interpretation()
			respuesta_clientes_ebitda_hint = empresa.respuesta_clientes_ebitda_hint()
			respuesta_clientes_resultado_interpretation = empresa.respuesta_clientes_resultado_interpretation()
			respuesta_clientes_resultado_hint = empresa.respuesta_clientes_resultado_hint()
		elif int(company_id)==1610:
			average_transfer_from_client = empresa.average_transfer_from_client()
			sells_sector = [{u'ejercicio': u'2011', 'c': 2180661.276511628}, {u'ejercicio': u'2012', 'c': 2062934.5268888888}, {u'ejercicio': u'2013', 'c': 2036585.5086363638}, {u'ejercicio': u'2014', 'c': 1840804.0434615384}]
			sells_me = [{u'ejercicio': u'2011', 'c': 2072914.685151515}, {u'ejercicio': u'2012', 'c': 1997092.5245454542}, {u'ejercicio': u'2013', 'c': 1920736.3365625}, {u'ejercicio': u'2014', 'c': 1786596.690588235}]
			ebitda_sector = [{u'ejercicio': u'2011', 'c': 122301.15116279075}, {u'ejercicio': u'2012', 'c': 144775.50600000002}, {u'ejercicio': u'2013', 'c': 102894.84340909087}, {u'ejercicio': u'2014', 'c': 103337.52038461539}]
			ebitda_me = [{u'ejercicio': u'2011', 'c': 112907.07303030306}, {u'ejercicio': u'2012', 'c': 124063.1478787879}, {u'ejercicio': u'2013', 'c': 84667.197499999995}, {u'ejercicio': u'2014', 'c': 94119.011176470583}]
			resultados_sector = [{u'ejercicio': u'2011', 'c': 83267.03534883722}, {u'ejercicio': u'2012', 'c': 88847.32644444442}, {u'ejercicio': u'2013', 'c': 48103.09454545455}, {u'ejercicio': u'2014', 'c': 37066.20846153845}]
			resultados_me = [{u'ejercicio': u'2011', 'c': 73000.65969696968}, {u'ejercicio': u'2012', 'c': 75194.46393939393}, {u'ejercicio': u'2013', 'c': 46659.145}, {u'ejercicio': u'2014', 'c': 44551.467058823528}]
			respuesta_clientes_ventas_interpretation = "En promedio, trabajas con clientes parecidos a los de tu competencia."
			respuesta_clientes_ventas_hint = "Bien! Si te interesa, puedes encontrar clientes de mayor tamaño utilizando nuestro motor de recomendaciones."
			respuesta_clientes_ebitda_interpretation = "En promedio, trabajas con clientes parecidos a los de tu competencia."
			respuesta_clientes_ebitda_hint = "Bien! Si te interesa, puedes encontrar clientes más  fuertes utilizando nuestro motor de recomendaciones."
			respuesta_clientes_resultado_interpretation = "En promedio, trabajas con clientes parecidos a los de tu competencia."
			respuesta_clientes_resultado_hint = "Bien! Si te interesa, puedes encontrar mejores clientes utilizando nuestro motor de recomendaciones."
			penetration = empresa.my_penetration_client()
			margen_comercial_sector_clientes = empresa.margen_comercial_sector_clientes()
		else:
			sells_sector = list(empresa.balance_clients_sells_avg_sector())
			sells_me = list(empresa.balance_clients_sells())
			ebitda_sector = list(empresa.balance_clients_ebitda_avg_sector())
			ebitda_me = list(empresa.balance_clients_ebitda())
			resultados_sector = list(empresa.balance_clients_resultado_avg_sector())
			resultados_me = list(empresa.balance_clients_resultado())
			penetration = empresa.my_penetration_client()
			margen_comercial_sector_clientes = empresa.margen_comercial_sector_clientes()
			average_transfer_from_client = empresa.average_transfer_from_client()
			respuesta_clientes_ventas_interpretation = empresa.respuesta_clientes_ventas_interpretation()
			respuesta_clientes_ventas_hint = empresa.respuesta_clientes_ventas_hint()
			respuesta_clientes_ebitda_interpretation = empresa.respuesta_clientes_ebitda_interpretation()
			respuesta_clientes_ebitda_hint = empresa.respuesta_clientes_ebitda_hint()
			respuesta_clientes_resultado_interpretation = empresa.respuesta_clientes_resultado_interpretation()
			respuesta_clientes_resultado_hint = empresa.respuesta_clientes_resultado_hint()

		diff_sells = (sells_me[len(sells_me)-1]['c'] - sells_sector[len(sells_sector)-1]['c'])/sells_sector[len(sells_sector)-1]['c']
		diff_ebitda = (ebitda_me[len(ebitda_me)-1]['c'] - ebitda_sector[len(ebitda_sector)-1]['c'])/ebitda_sector[len(ebitda_sector)-1]['c']
		diff_resultados = (resultados_me[len(resultados_me)-1]['c'] - resultados_sector[len(resultados_sector)-1]['c'])/resultados_sector[len(resultados_sector)-1]['c']
		ratio = 1-margen_comercial_sector_clientes

		if len(sells_me)>1:
			delta_ventas = (sells_me[len(sells_me)-1]['c'] - sells_me[len(sells_me)-2]['c'])/sells_me[len(sells_me)-2]['c']
		if len(ebitda_me)>1:
			delta_ebitda = (ebitda_me[len(ebitda_me)-1]['c'] - ebitda_me[len(ebitda_me)-2]['c'])/ebitda_me[len(ebitda_me)-2]['c']
		if len(resultados_me)>1:
			delta_resultados_explotacion = (resultados_me[len(resultados_me)-1]['c'] - resultados_me[len(resultados_me)-2]['c'])/resultados_me[len(resultados_me)-2]['c']

		hhi_clients_clients = empresa.hhi_clients_clients()
		context = {
			'company':empresa,
			'margen_comercial_sector_clientes': margen_comercial_sector_clientes,
			'ratio_comercial_sector_clientes': ratio,
			'respuesta_clientes_ventas_interpretation': respuesta_clientes_ventas_interpretation,
			'respuesta_clientes_ebitda_hint': respuesta_clientes_ebitda_hint,
			'respuesta_clientes_ventas_hint': respuesta_clientes_ventas_hint,
			'respuesta_clientes_ebitda_interpretation': respuesta_clientes_ebitda_interpretation,
			'respuesta_clientes_resultado_interpretation': respuesta_clientes_resultado_interpretation,
			'respuesta_clientes_resultado_hint': respuesta_clientes_resultado_hint,
			'average_transfer_from_client': average_transfer_from_client,
			'delta_ventas': delta_ventas,
			'delta_ebitda': delta_ebitda,
			'diff_sells': diff_sells,
			'diff_ebitda': diff_ebitda,
			'diff_resultados': diff_resultados,
			'delta_resultados_explotacion': delta_resultados_explotacion,
			'get_monthly_sells_amount': json.dumps(list(empresa.get_monthly_sells_amount()), cls=DjangoJSONEncoder),
			'get_sector_total_monthly_sells_amount': json.dumps(list(empresa.get_sector_total_monthly_sells_amount()), cls=DjangoJSONEncoder),
			'balance_sells_avg_sector': json.dumps(sells_sector, cls=DjangoJSONEncoder), #json.dumps(list(empresa.balance_clients_sells_avg_sector()), cls=DjangoJSONEncoder),
			'balance_sells': json.dumps(sells_me, cls=DjangoJSONEncoder), #json.dumps(list(empresa.balance_clients_sells()), cls=DjangoJSONEncoder),
			'balance_ebitda_avg_sector': json.dumps(ebitda_sector, cls=DjangoJSONEncoder), #json.dumps(list(empresa.balance_clients_ebitda_avg_sector()), cls=DjangoJSONEncoder),
			'balance_ebitda': json.dumps(ebitda_me, cls=DjangoJSONEncoder), #json.dumps(list(empresa.balance_clients_ebitda()), cls=DjangoJSONEncoder),
			'balance_resultado_avg_sector': json.dumps(resultados_sector, cls=DjangoJSONEncoder), #json.dumps(list(empresa.balance_clients_resultado_avg_sector()), cls=DjangoJSONEncoder),
			'balance_resultado': json.dumps(resultados_me, cls=DjangoJSONEncoder), #json.dumps(list(empresa.balance_clients_resultado()), cls=DjangoJSONEncoder),
			'penetration': penetration,
			'journey': request.session.get('journey'),
			'riesgo_impago_clientes': json.dumps(list(empresa.riesgo_impago_clientes()), cls=DjangoJSONEncoder),
			'riesgo_impago_clientes_sector': json.dumps(list(empresa.riesgo_impago_clientes_sector()), cls=DjangoJSONEncoder),
			'banco': request.session.get('banco')
			}

		return render(request, 'risk_cro/risk_client.html', context)
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/cro/", {})


@login_required
def CommercialProvidersRecommendationsView(request):
	if has_roborisk_permission(request.user) or request.user.is_superuser:
		company_id = request.session.get('company')
		empresa = Empresa.objects.filter(pk=company_id)
		empresa = empresa.prefetch_related('estados_financieros','transfers__destination_reference', 'destination_reference__origin_reference')[0]

		if int(company_id) == 1610:
			sells_sector = [{u'ejercicio': u'2011', 'c': 846283.4647849461}, {u'ejercicio': u'2012', 'c': 956645.75040462404}, {u'ejercicio': u'2013', 'c': 978471.62807453406}, {u'ejercicio': u'2014', 'c': 1056921.41805970157}]
			sells_me = [{u'ejercicio': u'2011', 'c': 1392696.61117647061}, {u'ejercicio': u'2012', 'c': 1534303.62062499998}, {u'ejercicio': u'2013', 'c': 1399953.46552631578}, {u'ejercicio': u'2014', 'c': 1491070.38647058822}]
			ebitda_sector = [{u'ejercicio': u'2011', 'c': 139361.97748407643}, {u'ejercicio': u'2012', 'c': 127984.25817891373}, {u'ejercicio': u'2013', 'c': 126471.11822525595}, {u'ejercicio': u'2014', 'c': 133865.1086259542}]
			ebitda_me = [{u'ejercicio': u'2011', 'c': 151794.07494505495}, {u'ejercicio': u'2012', 'c': 145185.49206521739}, {u'ejercicio': u'2013', 'c': 141847.803749999985}, {u'ejercicio': u'2014', 'c': 154199.451351351345}]
			resultados_sector = [{u'ejercicio': u'2011', 'c': 96543.67525477704}, {u'ejercicio': u'2012', 'c': 73854.49316293933}, {u'ejercicio': u'2013', 'c': 56644.12122866895}, {u'ejercicio': u'2014', 'c': 96736.3875572519}]
			resultados_me = [{u'ejercicio': u'2011', 'c': 153690.474505494498}, {u'ejercicio': u'2012', 'c': 102998.05847826087}, {u'ejercicio': u'2013', 'c': 70357.194875000005}, {u'ejercicio': u'2014', 'c': 132367.53648648648}]
			diff_sells = (sells_me[len(sells_me)-1]['c'] - sells_sector[len(sells_sector)-1]['c'])/sells_sector[len(sells_sector)-1]['c']
			diff_ebitda = (ebitda_me[len(ebitda_me)-1]['c'] - ebitda_sector[len(ebitda_sector)-1]['c'])/ebitda_sector[len(ebitda_sector)-1]['c']
			diff_resultados = (resultados_me[len(resultados_me)-1]['c'] - resultados_sector[len(resultados_sector)-1]['c'])/resultados_sector[len(resultados_sector)-1]['c']
			penetration = 0.04
			num_proveedores = empresa.get_providers().count()
			margen = 0.16
			ratio_comercial = 1- margen
			hhi_providers = empresa.hhi_providers()
			average_transfer_to_provider = 1267
		else:
			average_transfer_to_provider = empresa.average_transfer_to_provider()
			sells_sector = list(empresa.balance_providers_sells_avg_sector())
			sells_me = list(empresa.balance_providers_sells())
			ebitda_sector = list(empresa.balance_providers_ebitda_avg_sector())
			ebitda_me = list(empresa.balance_providers_ebitda())
			resultados_sector = list(empresa.balance_providers_resultado_avg_sector())
			resultados_me = list(empresa.balance_providers_resultado())
			penetration = empresa.my_penetration_provider()
			num_proveedores = empresa.get_providers().count()
			margen = empresa.margen_comercial_providers()
			ratio_comercial = 1- margen
			hhi_providers = empresa.hhi_providers()
			diff_sells = (sells_me[len(sells_me)-1]['c'] - sells_sector[len(sells_sector)-1]['c'])/sells_sector[len(sells_sector)-1]['c']
			diff_ebitda = (ebitda_me[len(ebitda_me)-1]['c'] - ebitda_sector[len(ebitda_sector)-1]['c'])/ebitda_sector[len(ebitda_sector)-1]['c']
			diff_resultados = (resultados_me[len(resultados_me)-1]['c'] - resultados_sector[len(resultados_sector)-1]['c'])/resultados_sector[len(resultados_sector)-1]['c']
			

		if len(sells_me)>1:
			delta_ventas = (sells_me[len(sells_me)-1]['c'] - sells_me[len(sells_me)-2]['c'])/sells_me[len(sells_me)-2]['c']
		if len(ebitda_me)>1:
			delta_ebitda = (ebitda_me[len(ebitda_me)-1]['c'] - ebitda_me[len(ebitda_me)-2]['c'])/ebitda_me[len(ebitda_me)-2]['c']
		if len(resultados_me)>1:
			delta_resultados_explotacion = (resultados_me[len(resultados_me)-1]['c'] - resultados_me[len(resultados_me)-2]['c'])/resultados_me[len(resultados_me)-2]['c']

		context = {
			'diff_sells': diff_sells,
			'average_transfer_to_provider': average_transfer_to_provider,
			'diff_ebitda': diff_ebitda,
			'diff_resultados': diff_resultados,
			'company':empresa,
			'num_proveedores': num_proveedores,
			'delta_ebitda': delta_ebitda,
			'delta_ventas': delta_ventas,
			'delta_resultados_explotacion': delta_resultados_explotacion,
			'hhi_providers': hhi_providers,
			'penetration': penetration,
			'margen': margen,
			'ratio_comercial': ratio_comercial,
			'get_monthly_buys_amount': json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder),
			'get_sector_total_monthly_buys_amount': json.dumps(list(empresa.get_sector_total_monthly_buys_amount()), cls=DjangoJSONEncoder),
			'balance_providers_sells_avg_sector': json.dumps(sells_sector, cls=DjangoJSONEncoder),
			'balance_providers_sells': json.dumps(sells_me, cls=DjangoJSONEncoder),
			'balance_providers_ebitda_avg_sector': json.dumps(ebitda_sector, cls=DjangoJSONEncoder),
			'balance_providers_ebitda': json.dumps(ebitda_me, cls=DjangoJSONEncoder),
			'balance_providers_resultado_avg_sector': json.dumps(resultados_sector, cls=DjangoJSONEncoder),
			'balance_providers_resultado': json.dumps(resultados_me, cls=DjangoJSONEncoder),
			'journey': request.session.get('journey'),
			'riesgo_impago_proveedores': json.dumps(list(empresa.riesgo_impago_proveedores()), cls=DjangoJSONEncoder),
			'riesgo_impago_providers_sector': json.dumps(list(empresa.riesgo_impago_providers_sector()), cls=DjangoJSONEncoder),
			'banco': request.session.get('banco')
			}

		return render(request, 'risk_cro/risk_providers.html', context)
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/cro/", {})

def FinancialRiskRecommendationsView(request):
	if has_roborisk_permission(request.user) or request.user.is_superuser:
		try:
			referrer = request.META['HTTP_REFERER']
			if 'intro' in referrer:
				request.session['journey'] = False
		except:
			request.session['journey'] = False

		print(request.session.get('journey'))

		company_id = request.session.get('company')
		company = Empresa.objects.filter(pk=company_id)
		company = company.prefetch_related('estados_financieros','cirbe','productos')[0]

		if int(company_id)==1610:
			deuda_ebitda = 0.9133
			deuda_largo = 154199.451351351345 * deuda_ebitda * 0.85
			deuda_corto = 154199.451351351345 * deuda_ebitda * 0.15
			ratio_corto_largo = deuda_corto / deuda_largo
			deuda_corto_pond = deuda_corto / 154199.451351351345
			dias_a_cobrar = 175
			dias_a_pagar = 58
			dias_a_pagar_sector = 85
			dias_a_cobrar_sector = 98
		else:
			deuda_ebitda = company.deuda_total_pond()
			deuda_largo = company.cirbe.largo_plazo_dispuesto
			deuda_corto = company.cirbe.corto_plazo_dispuesto
			ratio_corto_largo = company.ratio_corto_largo()
			deuda_corto_pond = company.deuda_corto_pond()
			dias_a_cobrar = company.dias_a_cobrar()
			dias_a_pagar = company.dias_a_pagar()
			dias_a_pagar_sector = company.dias_a_pagar_sector()
			dias_a_cobrar_sector = company.dias_a_cobrar_sector()
		try:
			ultimos_eeff = company.estados_financieros.reverse()[0]
		except:
			ultimos_eeff = Empresa()
		context = {
			'company':company,
			'dias_a_pagar_sector': dias_a_pagar_sector,
			'dias_a_cobrar_sector': dias_a_cobrar_sector,
			'deuda_corto_pond': deuda_corto_pond,
			'dias_a_pagar': dias_a_pagar,
			'dias_a_cobrar': dias_a_cobrar,
			'deuda_ebitda': deuda_ebitda,
			'deuda_largo': deuda_largo,
			'ratio_corto_largo': ratio_corto_largo,
			'deuda_corto': deuda_corto,
			'productos_variable': company.productos_con_tipo_variable().all(),
			'ultimos_eeff': ultimos_eeff,
			'journey': request.session.get('journey'),
			'banco': request.session.get('banco')
			}
		return render(request, 'risk_cro/risk_financial.html', context)
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/cro/", {})

def get_data_mekko(request, *args, **kwargs):
	data = dict([
		('agrup', 'Riesgo Negocio'),
		('data', [
			dict([
				('name','Riesgo Macro / Sectorial'),
				('value',5),
				('image', os.path.join(settings.STATIC_ROOT, 'images/Macroeconomico.jpg') ),
				('info', 'Analizamos la evolución macroeconómica y sectorial por ti. Te ayudamos a predecir posibles tendencias del mercado'),
				('fuertes', 'Tu crecimiento en facturación es superior al crecimiento macroeconómico/sectorial'),
				('mejorar', '<p></p>')])
			,
			dict([
				('name','Riesgo Competencia'),
				('value',15),
				('image', os.path.join(settings.STATIC_ROOT, 'images/Competencia.jpg') ),
				('info', 'Analizamos tu competencia por ti. Te ayudamos a visualizar las tendencias de tu competencia más directa'),
				('fuertes', 'Tu empresa muestra mejores resultados y evolución que tu competencia'),
				('mejorar', '<p>Tu competencia ha experimentado un crecimiento destacable en volumen de ventas en el útlimo ejercicio</p>')])
			,
			dict([
				('name','Riesgo Normativo'),
				('value',0),
				('image', os.path.join(settings.STATIC_ROOT, 'images/Competencia.jpg') ),
				('info', 'FER DESAPAREIXER'),
				('fuertes', 'Funcionalidad no disponible. Disculpa las molestias! Estamos trabajando para incluir este análisis y ofrecerte un mejor servicio'),
				('mejorar', 'Funcionalidad no disponible. Disculpa las molestias! Estamos trabajando para incluir este análisis y ofrecerte un mejor servicio')])
			])
		]), dict([
			('agrup', 'Riesgo Clientes'),
			('data', [
			dict([
				('name','Riesgo Demanda'),
				('value',10),
				('image', os.path.join(settings.STATIC_ROOT, 'images/demanda.jpg') ),
				('info', 'Analizamos tus clientes por ti. Te ayudamos a predecir posibles desviaciones en la demanda'),
				('fuertes', '<p>Tus clientes han crecido en el último año.</p><p>Tus clientes son parecidos en tamaño y resultados a los clientes de tu competencia.</p>'),
				('mejorar', '')])
			,
			dict([
				('name','Riesgo Fidelidad'),
				('value',20),
				('image', os.path.join(settings.STATIC_ROOT, 'images/Fidelidad.jpg') ),
				('info', 'Analizamos la fidelidad de tus clientes. Te ayudamos a medir el riesgo de fuga de tus clientes'),
				('fuertes', '<p>Tus clientes te son fieles, con relaciones duraderas y elevado índice de penetración</p>'),
				('mejorar', 'Tus clientes te tienen como proveedor principal, por lo que existe poco margen de crecimiento con ellos')])
			,
			dict([
				('name','Riesgo Solvencia'),
				('value',15),
				('image', os.path.join(settings.STATIC_ROOT, 'images/incumplimiento.jpg') ),
				('info', 'Analizamos la solvencia de tus clientes. Te ayudamos a medir el riesgo de impago de sus facturas'),
				('fuertes', '<p>Tus clientes tienen una solvencia en línea con la de los clientes de la competencia</p>'),
				('mejorar', '')])
			,
			dict([
				('name','Riesgo Concentración'),
				('value',20),
				('image', os.path.join(settings.STATIC_ROOT, 'images/concentration_clients.jpg') ),
				('info', 'Analizamos los riesgos de concentración de tus ventas. Te ayudamos a medir las necesidades de diversificación de tu negocio'),
				('fuertes', '<p>Buena diversificación en tus ventas, en un gran número de clientes</p>'),
				('mejorar', '<p>Baja diversificación de tus ventas, efectuadas en muy pocas provincias</p>')])
			])
		]), dict([
			('agrup', 'Riesgo Proveedores'),
			('data', [
			dict([
				('name','Riesgo Oferta'),
				('value',10),
				('image', os.path.join(settings.STATIC_ROOT, 'images/oferta.jpg') ),
				('info', 'Analizamos tus proveedores por ti. Te ayudamos a predecir posibles cambios en tus proveedores'),
				('fuertes', '<p>Tus proveedores son más fuertes y con mejores resultados que los proveedores de tu competencia</p>'),
				('mejorar', '<p>Tus proveedores han disminuido sus volúmenes de negocio en el último año</p>')])
			,
			dict([
				('name','Riesgo Solvencia'),
				('value',10),
				('image', os.path.join(settings.STATIC_ROOT, 'images/incumplimiento.jpg') ),
				('info', 'Analizamos la solvencia de tus proveedores. Te ayudamos a medir el riesgo de incumplimiento de sus obligaciones'),
				('fuertes', '<p>Tus proveedores tienen una solvencia en línea con la de los proveedores de la competencia</p>'),
				('mejorar', '<p>Tus proveedores han disminuido su volúmen de negocio en el último año</p>')])
			,
			dict([
				('name','Riesgo Concentración'),
				('value',10),
				('image', os.path.join(settings.STATIC_ROOT, 'images/concentration_providers.jpg') ),
				('info', 'Analizamos los riesgos de concentración de tus compras. Te ayudamos a medir las oportunidades de diversificación de proveedores'),
				('fuertes', '<p>Buena diversificación en tus compras, con un gran número de proveedores</p>'),
				('mejorar', '<p>Baja diversificación de tus compras, efectuadas en muy pocas provincias</p>')])
			])
		]), dict([
			('agrup', 'Riesgo Financiero'),
			('data', [
			dict([
				('name','Riesgo Acceso a inversión'),
				('value',5),
				('image', os.path.join(settings.STATIC_ROOT, 'images/acceso inversion.jpg') ),
				('info', 'Analizamos tu balance. Te ayudamos a entender como vemos tu solvencia para que puedas financiar tus inversiones a largo plazo'),
				('fuertes', '<p>Dispones de una buena salud financiera</p><p>Ratios de endeudadmiento globales sensiblemente inferiores a los de tu competencia</p>'),
				('mejorar', '<p></p>')])
			,
			dict([
				('name','Riesgo Acceso a circulante'),
				('value',10),
				('image', os.path.join(settings.STATIC_ROOT, 'images/acceso circulante.jpg') ),
				('info', 'Analizamos tu balance. Te ayudamos a entender como vemos tu solvencia para que puedas anticipar tu acceso financiación circulante en caso de imprevistos'),
				('fuertes', '<p>Dispones de una buena salud financiera</p><p>Ratios de endeudadmiento a corto plazo sensiblemente inferiores a los de tu competencia</p>'),
				('mejorar', '<p></p>')])
			,
			dict([
				('name','Riesgo Optimización del working capital'),
				('value',10),
				('image', os.path.join(settings.STATIC_ROOT, 'images/working capital.jpg') ),
				('info', 'Analizamos tus necesidades de working capital. Te ayudamos a optimizarlas y te ofrecemos soluciones de financiación'),
				('fuertes', '<p>Fluctuaciones en necesidades de working capital en línea con las de tu competencia</p>'),
				('mejorar', '<p></p>')])
			,
			dict([
				('name','Riesgo Divisa'),
				('value',5),
				('image', os.path.join(settings.STATIC_ROOT, 'images/divisa.jpg') ),
				('info', 'Analizamos tu exposición al mercado de divisas. Te ayudamos a medir y gestionar el riesgo asociado.'),
				('fuertes', '<p>Tienes poca exposición al mercado de divisas</p>'),
				('mejorar', '<p></p>')])
			,
			dict([
				('name','Riesgo Tipo de interés'),
				('value',5),
				('image', os.path.join(settings.STATIC_ROOT, 'images/riesog tipo interes.jpg') ),
				('info', 'Analizamos tu exposición al tipo de interés. Te ayudamos a medir y gestionar el riesgo asociado.'),
				('fuertes', '<p>Tienes poca exposición a los tipos de interés</p>'),
				('mejorar', '<p></p>')])
			])

		])
	return JsonResponse(data, safe=False)