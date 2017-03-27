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
from empresas.models import Empresa, EstadosFinancieros, RecommendedClients, RecommendedProviders
import random
from .permissions import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Prefetch

BANCO_PRESENTACION = 1

@login_required
def SearchView(request):
	if has_santander_permission(request.user):
		BANCO_PRESENTACION = 2
	elif has_sabadell_permission(request.user):
		BANCO_PRESENTACION = 1
	else:
		BANCO_PRESENTACION = 1
		
	if has_recommender_permission(request.user) or request.user.is_superuser:
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
			return render(request, "recommender/search.html", context)
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
			request.session['journey'] = False
			request.session.modified = True
			company = Empresa.objects.filter(pk=company_id)
			company = company.prefetch_related('estados_financieros','transfers')[0]
			return redirect("/recommender/", {'empresa': company, 'company': company})
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/pillstore/", {})

@login_required
def HomeView(request):
	if has_recommender_permission(request.user) or request.user.is_superuser:
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
				return render(request, "recommender/home.html", {'empresa': company, 'company': company})
			else:
				company_id = request.session.get('company')
				company = Empresa.objects.filter(pk=company_id)
				company = company.prefetch_related('estados_financieros','transfers')[0]
				return render(request, "recommender/home.html", {'empresa': company, 'company': company})
		except:
			company_id = request.session.get('company')
			company = Empresa.objects.filter(pk=company_id)
			company = company.prefetch_related('estados_financieros','transfers')[0]
			return render(request, "recommender/home.html", {'empresa': company, 'company': company})
	else:
		messages.warning(request, 'A pesar de tener un usuario activo, no tienes permiso para entrar en esta aplicación')
		return redirect("/pillstore/", {})

@login_required
def ClientView(request):

	try:
		referrer = request.META['HTTP_REFERER']
		if 'intro' in referrer or 'summary' in referrer:
			request.session['journey'] = False
	except:
		request.session['journey'] = False

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
	recommended_clients = recommended_clients.filter(similarity__gt=0)
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
			context = {
				"company": company, 
				"recommended_clients": recommended_clients[:50],
				"loading_times": request.session['recommended_clients_page'],
				'banco': request.session.get('banco')
			}
			return render(request, "recommender/cards_layout.html", context)
		else:
			recommended_clients = recommended_clients.exclude(clientes_recomendados__name=company.name)
			context = {
				"company": company, 
				"recommended_clients": recommended_clients[:50],
				"loading_times": request.session['recommended_clients_page'],
				'banco': request.session.get('banco')
			}
			return render(request, "recommender/cards_layout.html", context)

	context = {
		"company": company, 
		"title": "Recommended clients",
		'recommended_clients': recommended_clients[:50],
		"loading_times": request.session['recommended_clients_page'],
		'journey': request.session.get('journey'),
		'banco': request.session.get('banco')
	}
	return render(request, "recommender/recommended_clients.html", context)

"""-------------------------------------------------------"""
"""				PROVIDERS VIEWS 							  """
"""-------------------------------------------------------"""

# @login_required
def ProviderView(request):

	try:
		referrer = request.META['HTTP_REFERER']
		if 'intro' in referrer or 'summary' in referrer:
			request.session['journey'] = False
	except:
		request.session['journey'] = False

	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id)
	company = company.prefetch_related('providers_recommended__clientes_recomendados__estados_financieros','transfers')[0] #'estados_financieros','recommended','recommended__clientes_recomendados'

	recommended_providers = company.providers_recommended.all()  #company.get_recommended_providers()
	recommended_providers = recommended_providers.filter(similarity__gt=0)
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
			return render(request, "recommender/cards_layout.html", context)
		else:
			recommended_providers = company.recommended.all()
			context = {
				"company": company, 
				"recommended_providers": recommended_providers[:50],
				"loading_times": request.session['recommended_providers_page']
			}
			return render(request, "recommender/cards_layout.html", context)
	context = {
		"company": company, 
		"title": "Recommended providers",
		"recommended_providers": recommended_providers[:50],
		"loading_times": request.session['recommended_providers_page'],
		'journey': request.session.get('journey')
	}
	return render(request, "recommender/recommended_providers.html", context)


@login_required
def OpportunityClientsView(request):
	
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id).first()
	# company = company.prefetch_related('providers_recommended__clientes_recomendados__estados_financieros','transfers')[0] #'estados_financieros','recommended','recommended__clientes_recomendados'
	saved_clients = RecommendedClients.objects.filter(empresa=company).filter(clientes_recomendados__in=company.recommended_clients.all())
	context = {
		'company':company,
		'saved_clients': saved_clients
		}
	return render(request, 'recommender/opportunities_clients.html', context)

@login_required
def OpportunityProviderView(request):
	company_id = request.session.get('company')
	company = Empresa.objects.filter(pk=company_id).first()
	# company = company.prefetch_related('providers_recommended__clientes_recomendados__estados_financieros','transfers')[0] #'estados_financieros','recommended','recommended__clientes_recomendados'
	saved_providers = RecommendedProviders.objects.filter(empresa=company).filter(clientes_recomendados__in=company.recommended_providers.all())
	context = {
		'company':company,
		'saved_providers': saved_providers
		}
	return render(request, 'recommender/opportunities_providers.html', context)

@login_required
def EmpresaDetailView(request, pk=None):

	try:
		referrer = request.META['HTTP_REFERER']
		if 'intro' in referrer or 'summary' in referrer:
			request.session['journey'] = True
			if 'summary' in referrer:
				request.session['summary'] = True
	except:
		request.session['journey'] = False

	request.session.modified = True

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
	print(request.GET)
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
		buys_amount = json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder)
		buys_count = json.dumps(list(empresa.get_monthly_buys()), cls=DjangoJSONEncoder)
		sells_amount = json.dumps(list(empresa.get_monthly_sells_amount()), cls=DjangoJSONEncoder)
		sells_count = json.dumps(list(empresa.get_monthly_sells()), cls=DjangoJSONEncoder)
		titulo = 'Compras mensuales'
	elif key=='provider':
		buys_amount = json.dumps(list(empresa.get_monthly_buys_amount()), cls=DjangoJSONEncoder)
		buys_count = json.dumps(list(empresa.get_monthly_buys()), cls=DjangoJSONEncoder)
		sells_amount = json.dumps(list(empresa.get_monthly_sells_amount()), cls=DjangoJSONEncoder)
		sells_count = json.dumps(list(empresa.get_monthly_sells()), cls=DjangoJSONEncoder)
		titulo = 'Ventas mensuales'
	else:
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
		'journey': request.session.get('journey'),
		'summary': request.session.get('summary'),
		'banco': request.session.get('banco')
		}

	return render(request, 'recommender/empresa_detail.html', context)
