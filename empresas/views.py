from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.templatetags.staticfiles import static
import pandas as pd
from django.core.urlresolvers import reverse
from .models import Empresa, Transfer, EstadosFinancieros, Productos
import dateutil.parser
from .forms import TransferForm
import datetime
from django.utils import timezone
from random import randint
from faker import Factory
from django.conf import settings
from .als_recommender import *
import numpy
import os
import json
import random
import posixpath
from django.db.models import Avg, Max, Min, Count
from django.core.serializers.json import DjangoJSONEncoder

"""-------------------------------------------------------"""
"""				EMPRESAS VIEWS 							  """
"""-------------------------------------------------------"""

@method_decorator(login_required, name='dispatch')
class HomeView(View):
	def get(self, request, *args, **kwargs):
		try:
			del request.session['company']
			del request.session['recommended_clients_page']
		except:
			pass
		request.session.modified = True
		queryset = Empresa.objects.all()
		if request.session.get('company') is None:
			company = Empresa.objects.all()[randint(0, queryset.count() - 1)] #[865-1] #
			request.session['company'] = company
		else:
			company = request.session.get('company')
		return render(request, "empresas/empresas_home.html", {'company': company})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')

def EmpresasListView(request):
	latest_empresas_list = Empresa.objects.order_by('-created_at')[:10]
	context = {
		'latest_empresas_list':latest_empresas_list,
		'title': "Empresas"}
	return render(request, 'empresas/empresas_list.html', context)

def EmpresaDetailView(request, pk=None):
	
	empresa = get_object_or_404(Empresa, pk=pk)
	company = request.session.get('company')
	form = TransferForm()
	opp_client = request.GET.get("opp_client")
	print(opp_client)
	if opp_client:
		if opp_client=='true':
			company.recommended_clients.add(empresa)
			return HttpResponse("<small>Added to your opportunities</small>")
		else:
			company.recommended_clients.remove(empresa)
			return HttpResponse("<small>Removed from your opportunities</small>")
	checked_client = company.recommended_clients.filter(pk=empresa.pk).count()

	opp_provider = request.GET.get("opp_provider")
	print(opp_provider)
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
	for estado in empresa.estados_financieros.all():
		fechas.append(estado.ejercicio)
		try:
			depreciaciones.append(estado.depreciaciones)
			ebitda.append(estado.ebitda)
			resultado_explotacion.append(estado.resultado_explotacion)
			ventas.append(estado.ventas)
			amortizaciones.append(estado.amortizaciones)
		except:
			ventas.append(0)
			depreciaciones.append(0)
			ebitda.append(0)
			resultado_explotacion.append(0)
			amortizaciones.append(0)

	context = {
		'company': company,
		'empresa':empresa,
		'form': form,
		'ventas': json.dumps(ventas),
		'ebitda': json.dumps(ebitda),
		'depreciaciones': json.dumps(depreciaciones),
		'amortizaciones': json.dumps(amortizaciones),
		'resultado_explotacion': json.dumps(resultado_explotacion),
		'fechas': json.dumps(fechas),
		'checked_client': checked_client,
		'checked_providers': checked_providers}

	return render(request, 'empresas/empresa_detail.html', context)

def OpportunityClientsView(request):
	
	company = request.session.get('company')
	# empresas = company.opportunities.all()
	context = {
		'company':company
		}
	return render(request, 'empresas/opportunities_clients.html', context)

def OpportunityProviderView(request):
	
	company = request.session.get('company')
	# empresas = company.opportunities.all()
	context = {
		'company':company
		}
	return render(request, 'empresas/opportunities_providers.html', context)

def RecommendationsView(request):
	
	empresa = request.session.get('company')
	
	# territoriales_clientes = [empresa.in_my_region(empresa.get_clients()).count(), empresa.out_of_my_region(empresa.get_clients()).count()]
	# territoriales_proveedores = [empresa.in_my_region(empresa.get_providers()).count(), empresa.out_of_my_region(empresa.get_providers()).count()]
	# sector_territoriales_clientes = [empresa.in_my_region(empresa.get_qs_clients(empresa.get_sector_companies())).count(), empresa.out_of_my_region(empresa.get_qs_clients(empresa.get_sector_companies())).count()]
	# sector_territoriales_proveedores = [empresa.in_my_region(empresa.get_qs_providers(empresa.get_sector_companies())).count(), empresa.out_of_my_region(empresa.get_qs_providers(empresa.get_sector_companies())).count()]

	# sectores_clients, counts_sectores_clients = empresa.get_sectors(empresa.get_clients())
	# sectores_providers, counts_sectores_providers = empresa.get_sectors(empresa.get_providers())
	# mean_sectores_clients, mean_counts_sectores_clients = empresa.get_sectors(empresa.get_qs_clients(empresa.get_sector_companies()))
	# mean_sectores_providers, mean_counts_sectores_providers = empresa.get_sectors(empresa.get_qs_providers(empresa.get_sector_companies()))

	# your_monthly_sells = empresa.get_monthly_sells_amount()
	# for data in your_monthly_sells:
	# 	data['month'] = data['month'].strftime('%b')+'-'+data['month'].strftime('%y')
	
	# your_monthly_sells_amount = [d['c'] for d in your_monthly_sells]
	# your_monthly_sells_month = [d['month'] for d in your_monthly_sells]

	# sector_monthly_sells = empresa.get_sector_avg_monthly_sells_amount()
	# for data in sector_monthly_sells:
	# 	data['month'] = data['month'].strftime('%b')+'-'+data['month'].strftime('%y')
	
	# sector_monthly_sells_amount = [d['c'] for d in sector_monthly_sells]
	# sector_monthly_sells_month = [d['month'] for d in sector_monthly_sells]

	# your_ebitda = empresa.ebitda()
	# your_ebitda_amount = [d['c'] for d in your_ebitda]
	# your_ebitda_ejercicio = [d['ejercicio'] for d in your_ebitda]
	# sector_ebitda = empresa.ebitda_avg_sector()
	# sector_ebitda_amount = [d['c'] for d in sector_ebitda]
	# sector_ebitda_ejercicio = [d['ejercicio'] for d in sector_ebitda]

	# your_resultado_explotacion = empresa.resultado_explotacion()
	# your_resultado_explotacion_amount = [d['c'] for d in your_resultado_explotacion]
	# your_resultado_explotacion_ejercicio = [d['ejercicio'] for d in your_resultado_explotacion]
	# sector_resultado_explotacion = empresa.resultado_explotacion_avg_sector()
	# sector_resultado_explotacion_amount = [d['c'] for d in sector_resultado_explotacion]
	# sector_resultado_explotacion_ejercicio = [d['ejercicio'] for d in sector_resultado_explotacion]
	

	buttons = False

	context = {
		'company':empresa,
		# 'territoriales_proveedores': territoriales_proveedores,
		# 'territoriales_clientes': territoriales_clientes,
		# 'sector_territoriales_proveedores': sector_territoriales_proveedores,
		# 'sector_territoriales_clientes': sector_territoriales_clientes,
		# 'sectores_clients': json.dumps(sectores_clients),
		# 'counts_sectores_clients': counts_sectores_clients,
		# 'sectores_providers': json.dumps(sectores_providers),
		# 'counts_sectores_providers': counts_sectores_providers,
		# 'mean_sectores_clients': json.dumps(mean_sectores_clients),
		# 'mean_counts_sectores_clients': mean_counts_sectores_clients,
		# 'mean_sectores_providers': json.dumps(mean_sectores_providers),
		# 'mean_counts_sectores_providers': mean_counts_sectores_providers,
		# 'your_monthly_sells_amount': your_monthly_sells_amount,
		# 'your_monthly_sells_month': json.dumps(your_monthly_sells_month),
		# 'sector_monthly_sells_amount': sector_monthly_sells_amount,
		# 'sector_monthly_sells_month': json.dumps(sector_monthly_sells_month),
		# 'your_ebitda_amount': your_ebitda_amount,
		# 'your_ebitda_ejercicio': json.dumps(your_ebitda_ejercicio),
		# 'sector_ebitda_amount': sector_ebitda_amount,
		# 'sector_ebitda_ejercicio': json.dumps(sector_ebitda_ejercicio),
		# 'your_resultado_explotacion_amount': your_resultado_explotacion_amount,
		# 'your_resultado_explotacion_ejercicio': json.dumps(your_resultado_explotacion_ejercicio),
		# 'sector_resultado_explotacion_amount': sector_resultado_explotacion_amount,
		# 'sector_resultado_explotacion_ejercicio': json.dumps(sector_resultado_explotacion_ejercicio),
		'get_monthly_sells': json.dumps(list(empresa.get_monthly_sells()), cls=DjangoJSONEncoder),
		'get_monthly_sector_avg_sells': json.dumps(list(empresa.get_monthly_sector_avg_sells()), cls=DjangoJSONEncoder),
		'balance_sells_avg_sector': json.dumps(list(empresa.balance_clients_sells_avg_sector()), cls=DjangoJSONEncoder),
		'balance_sells': json.dumps(list(empresa.balance_clients_sells()), cls=DjangoJSONEncoder),
		'balance_ebitda_avg_sector': json.dumps(list(empresa.balance_clients_ebitda_avg_sector()), cls=DjangoJSONEncoder),
		'balance_ebitda': json.dumps(list(empresa.balance_clients_ebitda()), cls=DjangoJSONEncoder),
		'balance_resultado_avg_sector': json.dumps(list(empresa.balance_clients_resultado_avg_sector()), cls=DjangoJSONEncoder),
		'balance_resultado': json.dumps(list(empresa.balance_clients_resultado()), cls=DjangoJSONEncoder),
		'buttons': buttons
		}

	return render(request, 'empresas/recommendations.html', context)

"""-------------------------------------------------------"""
"""				TRANFERS VIEWS 							  """
"""-------------------------------------------------------"""

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

@login_required
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

@login_required
def ClientView(request):
	today = timezone.now().date()
	company = request.session.get('company')
	recommended_clients = company.recommended.all()
	sector, region, min_bill, comment = request.GET.get("sector"), request.GET.get("region"), request.GET.get("min_bill"), request.GET.get("comment")

	if request.session.get('recommended_clients_page') is None:
		request.session['recommended_clients_page'] = 1
	else:
		request.session['recommended_clients_page'] = request.session.get('recommended_clients_page') + 1

	if sector is not None or region is not None or min_bill is not None:
		if region=="true" or sector!="": 
			if region=="true":
				recommended_clients = company.recommended.filter(
					clientes_recomendados__territorial=company.territorial)
			if sector!="":
				# clientes_recomendados__cnae_2=sector, 
				recommended_clients = recommended_clients.filter(
					clientes_recomendados__cnae_2=sector)
			context = {
				"company": company, 
				"recommended_clients": recommended_clients,
				"loading_times": request.session['recommended_clients_page']
			}
			print(recommended_clients.count())
			return render(request, "empresas/cards_layout.html", context)
		else:
			recommended_clients = company.recommended.all()
			context = {
				"company": company, 
				"recommended_clients": recommended_clients,
				"loading_times": request.session['recommended_clients_page']
			}
			print(recommended_clients.count())
			return render(request, "empresas/cards_layout.html", context)

	context = {
		"company": company, 
		"title": "Recommended clients",
		"recommended_clients": recommended_clients,
		"today": today,
		"loading_times": request.session['recommended_clients_page']
	}
	print("Normal print...")
	print(company.recommended.all().count())
	return render(request, "empresas/recommended_clients.html", context)

"""-------------------------------------------------------"""
"""				PROVIDERS VIEWS 							  """
"""-------------------------------------------------------"""

@login_required
def ProviderView(request):
	today = timezone.now().date()
	company = request.session.get('company')
	recommended_clients = company.providers_recommended.all()
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
				"recommended_providers": recommended_providers,
				"loading_times": request.session['recommended_providers_page']
			}
			print(recommended_providers.count())
			return render(request, "empresas/cards_layout.html", context)
		else:
			recommended_providers = company.recommended.all()
			context = {
				"company": company, 
				"recommended_providers": recommended_providers,
				"loading_times": request.session['recommended_providers_page']
			}
			print(recommended_providers.count())
			return render(request, "empresas/cards_layout.html", context)

	context = {
		"company": company, 
		"title": "Recommended providers",
		"today": today,
		"loading_times": request.session['recommended_providers_page']
	}
	print("Normal print...")
	print(company.providers_recommended.all().count())
	return render(request, "empresas/recommended_providers.html", context)

"""-------------------------------------------------------"""
"""				DATA GENERATOR 							  """
"""-------------------------------------------------------"""

@login_required
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


@login_required
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


@login_required
def EstadosCreate(request):
	# ===============================================================
	# Importantdo datos financieros

	link = settings.DATA_FOLDER+'estados_financieros.csv'
	estados_financieros = pd.read_csv(link, sep=';', decimal=',', thousands='.', encoding='utf-8') # read empresas data
	estados_financieros = estados_financieros.astype(object).where(pd.notnull(estados_financieros), None)
	EstadosFinancieros.objects.all().delete()

	for index, row in estados_financieros.iterrows():
		print "%s: %s" %(index, str(row['ID_IDEFISC']))

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
		estados_financiero.ventas = float(row['VENTAS'])
		estados_financiero.depreciaciones = float(row['DEPRECIACIONES'])
		estados_financiero.amortizaciones = float(row['AMORTIZACIONES'])
		estados_financiero.ebitda = float(row['EBITDA'])
		estados_financiero.resultado_explotacion = float(row['RESULTADO_EXPLOTACION'])
		estados_financiero.existencias = float(row['EXISTENCIAS'])
		estados_financiero.deudores = float(row['DEUDORES_COMERCIALES'])
		estados_financiero.periodificaciones_ac = float(row['PERIODIFICACIONES_AC'])
		estados_financiero.provisiones_cp = float(row['PROVISIONES_CP'])
		estados_financiero.acreedores_comerciales = float(row['ACREEDORES_COMERCIALES'])
		estados_financiero.PERIODIFICACIONES_PC = float(row['PERIODIFICACIONES_PC'])
		estados_financiero.save()
	return HttpResponse("Estados financieros loaded")

@login_required
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
			print(index)
			print("I'am in!")
			Transfer.objects.bulk_create(transfers_list)
			transfers_list = []

	return HttpResponse("Transferencias loaded")

@login_required
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

# =====================================================================================

@method_decorator(login_required, name='dispatch')
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