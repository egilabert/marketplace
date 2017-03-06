#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.templatetags.staticfiles import static
import pandas as pd
from django.core.urlresolvers import reverse
from .models import Empresa, Transfer, EstadosFinancieros, Productos, CIRBE
import dateutil.parser
from .forms import TransferForm
import datetime
from django.utils import timezone
from random import randint
from faker import Factory
from django.conf import settings
from .als_recommender import *
from .item_based import *
import numpy
import os
import json
import random
import posixpath
from django.db.models import Avg, Max, Min, Count, Sum, Q
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Prefetch

"""-------------------------------------------------------"""
"""				EMPRESAS VIEWS 							  """
"""-------------------------------------------------------"""

# @login_required
def DebugView(request):
	# empresas = Empresa.objects.all()
	# for e in empresas:
	# 	rand = randint(0,1)
	# 	if rand > 0.3:
	# 		e.own_client = 'SÍ'
	# 	else:
	# 		e.own_client = 'NO'
	# 	e.save()

	# link = settings.DATA_FOLDER+'transferencias_cnae_v2.csv'
	# transferencias = pd.read_csv(link, sep=';', decimal=',', encoding='latin1')
	# transfer_count = transferencias.groupby(["REFERENCIA_1", "REFERENCIA_ORIGEN"]).IMPORTE.count().reset_index()

	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)[0]

	transferencias_clientes = Transfer.objects.filter(destination_reference=company).values('origin_reference', 'destination_reference').annotate(c=Count('amount'))
	transferencias_proveedores = Transfer.objects.filter(origin_reference=company).values('origin_reference', 'destination_reference').annotate(c=Count('amount'))
	transferencias_competencia_a_proveedores = Transfer.objects.filter(destination_reference__in=company.get_providers()).filter(origin_reference__in=company.get_sector_companies()).values('origin_reference', 'destination_reference').annotate(c=Count('amount'))
	transferencias_clientes_a_competencia = Transfer.objects.filter(destination_reference__in=company.get_sector_companies()).filter(origin_reference__in=company.get_clients()).values('origin_reference', 'destination_reference').annotate(c=Count('amount'))

	transferencias = list(transferencias_clientes)+list(transferencias_proveedores)+list(transferencias_competencia_a_proveedores)+list(transferencias_clientes_a_competencia)
	links = list(transferencias)
	links_list = list()
	for l in links:
		links_list.append({"source": l['origin_reference'], "target": l['destination_reference'], "value": l['c']})

	nodes = list(company.get_providers()) + list(company.get_clients()) + list(company.get_sector_companies())#+ list(additive) + list(additive2)
	nodes_list = [{'id': company.id, 'group': 1}]
	for n in nodes:
		if n in list(company.get_providers()):
			nodes_list.append({'id': n.id, 'group': 8})
		elif n in list(company.get_clients()):
			nodes_list.append({'id': n.id, 'group': 3})
		elif n in list(company.get_sector_companies()):
			nodes_list.append({'id': n.id, 'group': 4})

	network = {"nodes": nodes_list, "links": links_list}

	context = {
		'company': company,
		'network': json.dumps(network, cls=DjangoJSONEncoder),
		'rec': company.clients_of_sector_companies().exclude(id__in=company.get_clients()),
		'recommended_clients': company.get_recommended_clients(),
		'recommended_providers': company.get_recommended_providers(),
	}
	return render(request, "empresas/debugging_recommender.html", context)


# @login_required
def InformeView(request):
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)[0]
	context = {
		'company': company,
		'recommended_clients': company.recommended_clients.all(),
		'recommended_providers': company.recommended_providers.all(),
	}
	return render(request, "empresas/journey.html", context)

# @login_required
def SearchView(request):
	
	autofilter = dict()
	# company = Empresa.objects.filter(pk=990).first()
	# autofilter[company.name] = company.image
	# company = Empresa.objects.filter(pk=233).first()  
	# autofilter[company.name] = company.image
	# company = Empresa.objects.filter(pk=1610).first()
	# autofilter[company.name] = company.image
	company = Empresa.objects.all()
	for c in company:
		autofilter[c.name] = c.image

	context = {
		'autofilter': json.dumps(autofilter, cls=DjangoJSONEncoder),
		'buttons': False
	}
	return render(request, "empresas/search_company.html", context)

def IntroView(request):
	print('-------------')
	company = request.session['company']
	print(company)
	print('-------------')
	return render(request, "empresas/empresas_home.html", {'company': Empresa.objects.all()[company-1], 'buttons': False})

# @login_required
def HomeView(request):
	if request.POST and request.POST.get('journey1',None):
		try:
			del request.session['company']
			del request.session['recommended_clients_page']
		except:
			pass
		request.session.modified = True
		got_it = Empresa.objects.filter(pk=990).first()
		company = got_it.pk #1492 #randint(0, queryset.count() - 1) # # ## 865 865-1 
		request.session['company'] = company
		return HttpResponseRedirect(str(got_it.pk))

	elif request.POST and request.POST.get('journey2',None):
		try:
			del request.session['company']
			del request.session['recommended_clients_page']
		except:
			pass
		request.session.modified = True
		got_it = Empresa.objects.filter(pk=1610).first()
		company = got_it.pk #1492 #randint(0, queryset.count() - 1) # # ## 865 865-1 
		request.session['company'] = company
		return HttpResponseRedirect(str(got_it.pk))

	elif request.POST and request.POST.get('company_name',None):
		name = request.POST['company_name']

	try:
		del request.session['company']
		del request.session['recommended_clients_page']
	except:
		pass
	request.session.modified = True

	if request.session.get('company') is None:
		if request.user.username == "pmonras2":
			company = 865
		else:
			try:
				got_it = Empresa.objects.filter(name=name).first()
				company = got_it.pk #1492 #randint(0, queryset.count() - 1) # # ## 865 865-1
			except:
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		request.session['company'] = company
	else:
		try:
			company_id = request.session.get('company')
			company = Empresa.objects.filter(pk=company_id).first()
		except:
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	#return render(request, 'empresas/empresas_home.html', {})
	return HttpResponseRedirect(reverse('empresas:empresas_intro'))
	#return render(request, "empresas/journey.html", {'empresa': Empresa.objects.all()[company-1]})

# @login_required
def EmpresaDetailView(request, pk=None):

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

	form = TransferForm()
	opp_client = request.GET.get("opp_client")
	if opp_client:
		if opp_client=='true':
			company.recommended_clients.add(empresa)
			return HttpResponse("<small>Added to your opportunities</small>")
		else:
			company.recommended_clients.remove(empresa)
			return HttpResponse("<small>Removed from your opportunities</small>")
	checked_client = company.recommended_clients.filter(pk=empresa.pk).count()

	opp_provider = request.GET.get("opp_provider")
	if opp_provider:
		if opp_provider=='true':
			company.recommended_providers.add(empresa)
			return HttpResponse("<small>Added to your opportunities</small>")
		else:
			company.recommended_providers.remove(empresa)
			return HttpResponse("<small>Removed from your opportunities</small>")
	checked_providers = company.recommended_providers.filter(pk=empresa.pk).count()

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
	try:
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
	except:
		ventas.append(0)
		depreciaciones.append(0)
		ebitda.append(0)
		resultado_explotacion.append(0)
		amortizaciones.append(0)
		num_proveedores = empresa.get_providers().count()
		hhi_providers = empresa.hhi_providers()
		margen_comercial_sector_clientes = empresa.margen_comercial_sector_clientes()

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

	if key=='client':
		data = json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder)
		titulo = 'Compras mensuales'
	elif key=='provider':
		data = json.dumps(list(empresa.get_monthly_sells_amount()), cls=DjangoJSONEncoder)
		titulo = 'Ventas mensuales'
	else:
		data = json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder)
		titulo = 'Compras mensuales'

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

	print(empresa.clients_sector_by_sector())
	
	context = {
		'referrer': key,
		'delta_ventas': delta_ventas,
		'trabajadores': trabajadores,
		'delta_ebitda': delta_ebitda,
		'delta_resultados_explotacion': delta_resultados_explotacion,
		'company': company,
		'empresa':empresa,
		'form': form,
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
		'monthly_sells': data,
		'amortizaciones': json.dumps(amortizaciones),
		'resultado_explotacion': json.dumps(resultado_explotacion),
		'fechas': json.dumps(fechas),
		'checked_client': checked_client,
		'checked_providers': checked_providers,
		'get_monthly_buys_amount': json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder),
		'get_sector_total_monthly_buys_amount': json.dumps(list(empresa.get_sector_total_monthly_buys_amount()), cls=DjangoJSONEncoder),
		'balance_sells_avg_sector': json.dumps(sells_sector, cls=DjangoJSONEncoder),
		'balance_sells': json.dumps(sells_me, cls=DjangoJSONEncoder),
		'balance_ebitda_avg_sector': json.dumps(ebitda_sector, cls=DjangoJSONEncoder),
		'balance_ebitda': json.dumps(ebitda_me, cls=DjangoJSONEncoder),
		'balance_resultado_avg_sector': json.dumps(resultados_sector, cls=DjangoJSONEncoder),
		'balance_resultado': json.dumps(resultados_me, cls=DjangoJSONEncoder),
		}

	return render(request, 'empresas/empresa_detail.html', context)

# @login_required
def OpportunityClientsView(request):
	
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id).first()
	context = {
		'company':company
		}
	return render(request, 'empresas/opportunities_clients.html', context)

# @login_required
def FinancialRiskRecommendationsView(request):
	
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
		'ultimos_eeff': ultimos_eeff
		}
	return render(request, 'empresas/financial_risk.html', context)

# @login_required
def FAQView(request):
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)
	context = {
		'company':company
	}
	return render(request, 'empresas/faq.html', context)

# @login_required
def ClientRiskRecommendationsView(request):
	
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
	context = {
		'company':company,
		'penetracion': penetracion,
		'riesgo_impago_clientes': json.dumps(list(company.riesgo_impago_clientes()), cls=DjangoJSONEncoder),
		'riesgo_impago_clientes_sector': json.dumps(list(company.riesgo_impago_clientes_sector()), cls=DjangoJSONEncoder),
		'get_monthly_buys': json.dumps(list(company.get_monthly_buys_amount()), cls=DjangoJSONEncoder),
		'get_monthly_sector_avg_buys': json.dumps(list(company.get_sector_total_monthly_buys_amount()), cls=DjangoJSONEncoder),
		'productos_variable': company.productos_con_tipo_variable().all(),
		'ultimos_eeff': ultimos_eeff
		}
	return render(request, 'empresas/risk_client.html', context)

# @login_required
def ProviderRiskRecommendationsView(request):
	
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)
	company = company.prefetch_related('estados_financieros','cirbe','productos')[0]
	try:
		ultimos_eeff = company.estados_financieros.reverse()[0]
	except:
		ultimos_eeff = Empresa()
	if int(company_id)==1610:
		dependencia = 0.04
		hhi_providers = company.hhi_providers()
		proveedores = company.get_providers().count()
	else:
		dependencia = company.my_penetration_provider()
		hhi_providers = company.hhi_providers()
		proveedores = company.get_providers().count()
	context = {
		'company':company,
		'dependencia': dependencia,
		'proveedores': proveedores,
		'hhi_providers': hhi_providers,
		'riesgo_impago_proveedores': json.dumps(list(company.riesgo_impago_proveedores()), cls=DjangoJSONEncoder),
		'riesgo_impago_providers_sector': json.dumps(list(company.riesgo_impago_providers_sector()), cls=DjangoJSONEncoder),
		'get_monthly_sells': json.dumps(list(company.get_monthly_sells_amount()), cls=DjangoJSONEncoder),
		'get_monthly_sector_avg_sells': json.dumps(list(company.get_sector_total_monthly_sells_amount()), cls=DjangoJSONEncoder),
		'productos_variable': company.productos_con_tipo_variable().all(),
		'ultimos_eeff': ultimos_eeff
		}
	return render(request, 'empresas/risk_providers.html', context)

# @login_required
def OpportunityProviderView(request):
	
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)
	context = {
		'company':company
		}
	return render(request, 'empresas/opportunities_providers.html', context)

# @login_required
def CommercialProvidersRecommendationsView(request):
	company_id = request.session.get('company')
	empresa = Empresa.objects.filter(pk=company_id)
	empresa = empresa.prefetch_related('estados_financieros','transfers__destination_reference', 'destination_reference__origin_reference',
	Prefetch(
        "transfers__destination_reference",
        queryset=Empresa.objects.filter(transfers__destination_reference=empresa[0]).annotate(Count('name', distinct=True)),
        to_attr="clients"
    ))[0]

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
		}

	return render(request, 'empresas/comercial_recommendations_providers.html', context)

# @login_required
def CommercialClientsRecommendationsView(request):
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
		'penetration': penetration
		}

	return render(request, 'empresas/comercial_recommendations_clients.html', context)

"""-------------------------------------------------------"""
"""				TRANFERS VIEWS 							  """
"""-------------------------------------------------------"""

# @login_required
def TransferListView(request):
	latest_tranfers_list = Transfer.objects.order_by('-operation_data')[:10]
	context = {
		'latest_tranfers_list':latest_tranfers_list,
		'title': "Transferencias realizada"}
	return render(request, 'empresas/transfer_list.html', context)

def TransferDetailView(request, transfer_id):
	transfer = get_object_or_404(Transfer, pk=transfer_id)
	context = {'transfer':transfer}
	return render(request, 'empresas/transfer_detail.html', context)

# @login_required
def TrasferCreateView(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    form = TransferForm(request.POST)
    if form.is_valid():
        concept = form.cleaned_data['concept']
        amount = form.cleaned_data['amount']
        balance = form.cleaned_data['balance']
        destination_reference = form.cleaned_data['destination_reference']

        transfer = Transfer()
        transfer.origin_reference = empresa
        transfer.operation_data = datetime.datetime.now()
        transfer.value_date = datetime.datetime.now()
        transfer.concept = concept
        transfer.amount = amount
        transfer.balance = balance
        transfer.destination_reference = destination_reference
        transfer.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('empresas:empresa_detail', args=(empresa.id,)))

    return render(request, 'empresas/empresa_detail.html', {'empresa': empresa, 'form': form})

"""-------------------------------------------------------"""
"""				CLIENTS VIEWS 							  """
"""-------------------------------------------------------"""

# @login_required
def ClientView(request):

	today = timezone.now().date()
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)
	company = company.prefetch_related('recommended__clientes_recomendados','transfers',
	Prefetch(
        "estados_financieros",
        queryset=EstadosFinancieros.objects.filter(empresa=company),
        to_attr="ultimos_estados_financieros"
    ))[0]

	sector, region, min_bill, comment = request.GET.get("sector"), request.GET.get("region"), request.GET.get("min_bill"), request.GET.get("comment")

	if request.session.get('recommended_clients_page') is None:
		request.session['recommended_clients_page'] = 1
	else:
		request.session['recommended_clients_page'] = request.session.get('recommended_clients_page') + 1

	recommended_clients = company.recommended.all() #company.get_recommended_clients()

	if sector is not None or region is not None or min_bill is not None:
		if region=="true" or sector!="": 
			if region=="true":
				recommended_clients = recommended_clients.exclude(
					clientes_recomendados__territorial=company.territorial)
			else:
				recommended_clients = recommended_clients.filter(
					clientes_recomendados__territorial=company.territorial)
			if sector != "":
				recommended_clients = recommended_clients.filter(
					clientes_recomendados__cnae_2=sector)
			print(recommended_clients)
			context = {
				"company": company, 
				"recommended_clients": recommended_clients[:50],
				"loading_times": request.session['recommended_clients_page']
			}
			return render(request, "empresas/cards_layout.html", context)
		else:
			recommended_clients = recommended_clients.exclude(clientes_recomendados__name=company.name)
			context = {
				"company": company, 
				"recommended_clients": recommended_clients[:50],
				"loading_times": request.session['recommended_clients_page']
			}
			return render(request, "empresas/cards_layout.html", context)
	print('nada')
	context = {
		"company": company, 
		"title": "Recommended clients",
		"today": today,
		'recommended_clients': recommended_clients[:50],
		"loading_times": request.session['recommended_clients_page']
	}
	return render(request, "empresas/recommended_clients.html", context)

"""-------------------------------------------------------"""
"""				PROVIDERS VIEWS 							  """
"""-------------------------------------------------------"""

# @login_required
def ProviderView(request):
	today = timezone.now().date()
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)
	company = company.prefetch_related('providers_recommended__clientes_recomendados__estados_financieros','transfers')[0] #'estados_financieros','recommended','recommended__clientes_recomendados'

	recommended_providers = company.get_recommended_providers()  #company.providers_recommended.all()
	sector, region, min_bill, comment = request.GET.get("sector"), request.GET.get("region"), request.GET.get("min_bill"), request.GET.get("comment")

	if request.session.get('recommended_providers_page') is None:
		request.session['recommended_providers_page'] = 1
	else:
		request.session['recommended_providers_page'] = request.session.get('recommended_providers_page') + 1

	if sector is not None or region is not None or min_bill is not None:
		if region=="true" or sector!="": 
			if region=="true":
				recommended_providers = company.recommended.filter(
					clientes_recomendados__territorial=company.territorial)
			if sector!="":
				# clientes_recomendados__cnae_2=sector, 
				recommended_providers = recommended_providers.filter(
					clientes_recomendados__cnae_2=sector)
			context = {
				"company": company, 
				"recommended_providers": recommended_providers[:50],
				"loading_times": request.session['recommended_providers_page']
			}
			return render(request, "empresas/cards_layout.html", context)
		else:
			recommended_providers = company.recommended.all()
			context = {
				"company": company, 
				"recommended_providers": recommended_providers[:50],
				"loading_times": request.session['recommended_providers_page']
			}
			return render(request, "empresas/cards_layout.html", context)
	print(recommended_providers)
	context = {
		"company": company, 
		"title": "Recommended providers",
		"recommended_providers": recommended_providers[:50],
		"today": today,
		"loading_times": request.session['recommended_providers_page']
	}
	return render(request, "empresas/recommended_providers.html", context)

"""-------------------------------------------------------"""
"""				DATA GENERATOR 							  """
"""-------------------------------------------------------"""

@staff_member_required
def EmpresasCreate(request):
	# ===============================================================

	# Importantdo datos de empresa
	fake = Factory.create('es_ES')
	link = settings.DATA_FOLDER+'empresas_ok.csv'
	empresas = pd.read_csv(link, sep=';', decimal=',', encoding='latin1') # read empresas data
	Empresa.objects.all().delete()
	for index, row in empresas.iterrows():
		empresa = Empresa()
		empresa.fiscal_id = row['ID_IDEFISC']
		empresa.name = row['NOMBRE']
		empresa.email = fake.email()
		empresa.contact_person = fake.name()
		empresa.state_name = fake.state_name()
		empresa.latitude = fake.latitude()
		empresa.longitude = fake.longitude()
		empresa.phone = fake.phone_number()
		empresa.address = fake.address()
		empresa.image = random_image('images/TBR/Resized/')
		try:
			empresa.data_date = dateutil.parser.parse(row['ID_FCH_DATOS'])
		except:
			pass
		try:
			empresa.creation_date = dateutil.parser.parse(row['FECHA_NACIMIENTO'])
		except:
			pass
		empresa.sector = row['Sector']
		empresa.cnae = row['CNAE']
		empresa.cnae_2 = row['CNAE_2']
		empresa.cnae_num = row['CNAE_NUM']
		empresa.group_name = row['NOM_GRUP']
		try:
			empresa.hats_date = dateutil.parser.parse(row['FECHA_HATS'])
		except:
			pass
		empresa.hats_alert = row['ALERTA_HATS']
		empresa.concursal = row['CONCURSAL']
		empresa.recent_creation = row['RECIENTE_CREACION']
		empresa.segment = row['SEGMENTO_GESTION']
		empresa.subsegment = row['SUBSEGMENTO_GESTION']
		empresa.territorial = row['DE_CORTA_TERRITORIAL_GEST']
		empresa.regional = row['NOMBRE_REGIONAL_GEST']
		empresa.centro_gestor = row['NOMBRE_CENTRO_GEST']
		empresa.oficina = row['OFICINA']
		empresa.save()
	
	return HttpResponse("Empresas loaded")


@staff_member_required
def ProductosCreate(request):
	fake = Factory.create('es_ES')

	# Importantdo datos financieros......
	link = settings.DATA_FOLDER+'productos.csv'
	productos = pd.read_csv(link, sep=';', decimal=',', thousands='.', encoding='latin1') # read empresas data
	Productos.objects.all().delete()

	productos = productos.astype(object).where(pd.notnull(productos), None)
	for index, row in productos.iterrows():
		producto = Productos()
		try:
			producto.empresa = Empresa.objects.get(fiscal_id=str(row['ID_IDEFISC']))
		except Empresa.DoesNotExist:
				producto.empresa = None
		try:
			producto.fecha_datos = dateutil.parser.parse(row['ID_FCH_DATOS'])
		except:
			pass
		try:
			producto.numero_persona = row['NUMPER']
		except:
			producto.numero_persona = None

		producto.tipo_producto = row['ID_TIPO_PRODUCTO_2']
		producto.producto = row['PRODUCTE']
		producto.desc_producto = row['DESC_PR']
		producto.id_contrato = row['ID_CONTRATO']
		producto.concedido = row['CONCEDIDO']
		producto.dispuesto = row['DISPUESTO']
		producto.impagado = row['IMPAGADO']
		producto.dias_impago = row['DIAS_IMPAGO']
		producto.cuotas_impagadas = row['CUOTAS_IMPAGADAS']
		try:
			producto.fecha_formalizacion = dateutil.parser.parse(row['FECHA_FORMALIZACION'])
		except:
			pass
		try:
			producto.fecha_vencimiento = dateutil.parser.parse(row['FECHA_VENCIMIENTO'])
		except:
			pass
		producto.concedido_inicial = row['CONCEDIDO_INI']
		producto.capital_pdte = row['CAPITAL_PDTE']
		producto.interes_revisado = row['INTERES_REV']
		producto.cuotas_total = row['CUOTAS_TOTAL']
		producto.cuota_anual = row['CUOTA_ANUAL_IMPPRXCUO']
		producto.cuota = row['IMPPRXCUO']
		producto.garantia_hip = row['HIPOTECARIO']
		producto.sit_contable = row['TIP_DOT_RECALC_RECOD']
		producto.segmento_gestion = row['SEGMENTO_GESTION']
		if row['Refi']==1:
			producto.refinanciado = True
		else:
			producto.refinanciado = False
		producto.save()
	return HttpResponse("Productos loaded")


@staff_member_required
def EstadosCreate(request):
	# ===============================================================
	# Importantdo datos financieros

	link = settings.DATA_FOLDER+'estados_financieros.csv'
	estados_financieros = pd.read_csv(link, sep=';', decimal=',', thousands='.', encoding='utf-8') # read empresas data
	estados_financieros = estados_financieros.astype(object).where(pd.notnull(estados_financieros), None)
	EstadosFinancieros.objects.all().delete()

	for index, row in estados_financieros.iterrows():
		estados_financiero = EstadosFinancieros()
		try:
			estados_financiero.empresa = Empresa.objects.get(fiscal_id=str(row['ID_IDEFISC']))
		except Empresa.DoesNotExist:
				estados_financiero.empresa = None
		try:
			estados_financiero.ejercicio = str(row['ID_EJER_BALAN'])
		except:
			pass
		try:
			estados_financiero.fecha_balance = dateutil.parser.parse(row['ID_FCH_BALANCE'])
		except:
			pass
		estados_financiero.ventas = float(row['VENTAS'] or 0)
		estados_financiero.depreciaciones = float(row['DEPRECIACIONES'] or 0)
		estados_financiero.amortizaciones = float(row['AMORTIZACIONES'] or 0)
		estados_financiero.ebitda = float(row['EBITDA'] or 0)
		estados_financiero.resultado_explotacion = float(row['RESULTADO_EXPLOTACION'] or 0)
		estados_financiero.existencias = float(row['EXISTENCIAS'] or 0)
		estados_financiero.deudores = float(row['DEUDORES_COMERCIALES'] or 0)
		estados_financiero.periodificaciones_ac = float(row['PERIODIFICACIONES_AC'] or 0)
		estados_financiero.provisiones_cp = float(row['PROVISIONES_CP'] or 0)
		estados_financiero.acreedores_comerciales = float(row['ACREEDORES_COMERCIALES'] or 0)
		estados_financiero.PERIODIFICACIONES_PC = float(row['PERIODIFICACIONES_PC'] or 0)
		estados_financiero.save()
	return HttpResponse("Estados financieros loaded")

@staff_member_required
def CirbeCreate(request):
	# ===============================================================
	# Importantdo datos financieros

	link = settings.DATA_FOLDER+'cirbe.csv'
	cirbe_data = pd.read_csv(link, sep=';', decimal=',', thousands='.', encoding='utf-8') # read empresas data
	cirbe_data = cirbe_data.astype(object).where(pd.notnull(cirbe_data), None)
	CIRBE.objects.all().delete()

	for index, row in cirbe_data.iterrows():
		cirbe = CIRBE()
		try:
			cirbe.empresa = Empresa.objects.get(fiscal_id=str(row['ID_IDEFISC']))
			print(cirbe.empresa)
		except Empresa.DoesNotExist:
			print('================================= Allahu!!!! ==================================')
			cirbe.empresa = None
		cirbe.cirbe_concedido = int(row['CIRBE_CONCEDIDO'] or 0)
		cirbe.cirbe_dispuesto = int(row['CIRBE_DISPUESTO'] or 0)
		cirbe.largo_plazo_concedido = int(row['LP_C'] or 0)
		cirbe.largo_plazo_dispuesto = int(row['LP_D'] or 0)
		cirbe.corto_plazo_concedido = int(row['CP_C'] or 0)
		cirbe.corto_plazo_dispuesto = int(row['CP_D'] or 0)
		cirbe.d_concedido = int(row['D_C'] or 0)
		cirbe.d_dispuesto = int(row['D_D'] or 0)
		cirbe.avales_concedido = int(row['AV_CONCEDIDO'] or 0)
		cirbe.avales_dispuesto = int(row['AV_D'] or 0)
		cirbe.leasing_concedido = int(row['LEAS_CONCEDIDO'] or 0)
		cirbe.leasing_dispuesto = int(row['L_D'] or 0)
		cirbe.sr_concedido = int(row['SR_C'] or 0)
		cirbe.sr_dispuesto = int(row['SR_D'] or 0)
		cirbe.moroso = int(row['MOROSO'] or 0)
		cirbe.save()

	return HttpResponse("CIRBE loaded")

@staff_member_required
def TranfersCreate(request):
	# ===============================================================
	# Importantdo transferencias.......
	fake = Factory.create('es_ES')
	link = settings.DATA_FOLDER+'transferencias_cnae_v2.csv'
	transferencias = pd.read_csv(link, sep=';', decimal=',', encoding='latin1')
	Transfer.objects.all().delete()
	transfers_list = []
	for index, row in transferencias.iterrows():
		transfer = Transfer()
		try:
			transfer.operation_data = dateutil.parser.parse(row['FECHA_OPER'])
		except:
			pass
		try:
			transfer.value_date = dateutil.parser.parse(row['FECHA_VALOR'])
		except:
			pass
		transfer.concept = fake.sentence(nb_words=6, variable_nb_words=True)
		transfer.amount = row['IMPORTE']
		transfer.balance = row['SALDO']
		transfer.destination_reference = Empresa.objects.get(fiscal_id=str(row['REFERENCIA_1']))
		transfer.origin_reference = Empresa.objects.get(fiscal_id=str(row['REFERENCIA_ORIGEN']))
		transfers_list.append(transfer)
		if (index % 10000==0) and (index!=0):
			Transfer.objects.bulk_create(transfers_list)
			transfers_list = []

	return HttpResponse("Transferencias loaded")

@staff_member_required
def RecommendationsCreate(request):
	# ===============================================================

	# Generando recomendaciones.......

	link = settings.DATA_FOLDER+'transferencias_cnae_v2.csv'
	transferencias = pd.read_csv(link, sep=';', decimal=',', encoding='latin1')
	RecommendedClients.objects.all().delete()
	RecommendedProviders.objects.all().delete()
	# Empresa.objects.clients.all().delete()
	# Empresa.objects.providers.all().delete()
	calculate_similar_artists(transferencias, "similar-artists.tsv",
                          factors=50, regularization=0.01,
                          iterations=15,
                          exact=False, trees=20,
                          use_native=True,
                          dtype=numpy.float64)
	return HttpResponse("Recommendations loaded")

@staff_member_required
def ContentBasedCreate(request):
	# ===============================================================

	# Generando recomendaciones.......
	content_based_similarity()
	return HttpResponse("Recommendations loaded")
	

@staff_member_required
def CompaniesCleanning(request):
	# ===============================================================
	# Generando recomendaciones.......
	empresas = Empresa.objects.all()
	return HttpResponse("Recommendations loaded")

# =====================================================================================

@method_decorator(staff_member_required, name='dispatch')
class DataGenerator(View):

	def get(self, request, *args, **kwargs):
  		return render(request, "empresas/dataset_generator.html", {})

 # =====================================================================================
# Helper function

def is_image_file(filename):
    """Does `filename` appear to be an image file?"""
    img_types = [".jpg", ".jpeg", ".png", ".gif"]
    ext = os.path.splitext(filename)[1]
    return ext in img_types

def random_image(path):
    fullpath = os.path.join(settings.STATIC_ROOT, path)
    filenames = [f for f in os.listdir(fullpath) if is_image_file(f)]
    pick = random.choice(filenames)
    return posixpath.join(settings.STATIC_URL, path, pick)