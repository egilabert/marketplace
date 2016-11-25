from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.templatetags.staticfiles import static
import pandas as pd
from django.core.urlresolvers import reverse
from .models import Empresa, Transfer
import dateutil.parser
from .forms import TransferForm
import datetime
from django.utils import timezone
from random import randint
from faker import Factory
from .als_recommender import *
import numpy

"""-------------------------------------------------------"""
"""				EMPRESAS VIEWS 							  """
"""-------------------------------------------------------"""

@method_decorator(login_required, name='dispatch')
class HomeView(View):
	def get(self, request, *args, **kwargs):
		del request.session['company']
		request.session.modified = True
		queryset = Empresa.objects.all()
		if request.session.get('company') is None:
			company = Empresa.objects.all()[randint(0, queryset.count() - 1)]
			request.session['company'] = company
		else:
			company = request.session.get('company')
		return render(request, "empresas_home.html", {'company': company})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')

def EmpresasListView(request):
	latest_empresas_list = Empresa.objects.order_by('-created_at')[:10]
	context = {
		'latest_empresas_list':latest_empresas_list,
		'title': "Empresas"}
	return render(request, 'empresas/empresas_list.html', context)

def EmpresaDetailView(request, empresa_id):
	
	empresa = get_object_or_404(Empresa, pk=empresa_id)
	form = TransferForm()
	context = {
		'empresa':empresa,
		'form': form}
	return render(request, 'empresas/empresa_detail.html', context)

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
	context = {
		"company": company, 
		"title": "Recommended clients",
		"today": today,
	}
	
	return render(request, "empresas/recommended_clients.html", context)

"""-------------------------------------------------------"""
"""				DATA GENERATOR 							  """
"""-------------------------------------------------------"""

@method_decorator(login_required, name='dispatch')
class DataGenerator(View):

	def get(self, request, *args, **kwargs):
		# fake = Factory.create('es_ES')

		# # Importantdo datos de empresa
		# link = static('data/empresas.csv')
		# empresas = pd.read_csv("."+link, sep=';', decimal=',', encoding='latin1') # read empresas data
		# Empresa.objects.all().delete()
		# for index, row in empresas.iterrows():
		# 	empresa = Empresa()
		# 	empresa.fiscal_id = row['ID_IDEFISC']
		# 	empresa.name = row['NOMBRE']
		# 	empresa.email = fake.email()
		# 	try:
		# 		empresa.data_date = dateutil.parser.parse(row['ID_FCH_DATOS'])
		# 	except:
		# 		pass
		# 	try:
		# 		empresa.creation_date = dateutil.parser.parse(row['FECHA_NACIMIENTO'])
		# 	except:
		# 		pass
		# 	empresa.sector = row['Sector']
		# 	empresa.cnae = row['CNAE']
		# 	empresa.group_name = row['NOM_GRUP']
		# 	try:
		# 		empresa.hats_date = dateutil.parser.parse(row['FECHA_HATS'])
		# 	except:
		# 		pass
		# 	empresa.hats_alert = row['ALERTA_HATS']
		# 	empresa.concursal = row['CONCURSAL']
		# 	empresa.recent_creation = row['RECIENTE_CREACION']
		# 	empresa.segment = row['SEGMENTO_GESTION']
		# 	empresa.subsegment = row['SUBSEGMENTO_GESTION']
		# 	empresa.territorial = row['DE_CORTA_TERRITORIAL_GEST']
		# 	empresa.regional = row['NOMBRE_REGIONAL_GEST']
		# 	empresa.centro_gestor = row['NOMBRE_CENTRO_GEST']
		# 	empresa.oficina = row['OFICINA']
		# 	empresa.save()

		# # Importantdo transferencias.......
		# link = static('data/transferencias.csv')
		# transferencias = pd.read_csv("."+link, sep=';', decimal=',', encoding='latin1')
		# Transfer.objects.all().delete()
		# for index, row in transferencias.iterrows():
		# 	transfer = Transfer()
		# 	try:
		# 		transfer.operation_data = dateutil.parser.parse(row['FECHA_OPER'])
		# 	except:
		# 		pass
		# 	try:
		# 		transfer.value_date = dateutil.parser.parse(row['FECHA_VALOR'])
		# 	except:
		# 		pass
		# 	transfer.concept = fake.sentence(nb_words=6, variable_nb_words=True)
		# 	transfer.amount = row['IMPORTE']
		# 	transfer.balance = row['SALDO']
		# 	transfer.destination_reference = Empresa.objects.get(fiscal_id=str(row['REFERENCIA_1']))
		# 	transfer.origin_reference = Empresa.objects.get(fiscal_id=str(row['REFERENCIA_ORIGEN']))
		# 	transfer.save()

		# # Generando recomendaciones.......
		# link = static('data/transferencias.csv')
		# transferencias = pd.read_csv("."+link, sep=';', decimal=',', encoding='latin1')
		# RecommendedClients.objects.all().delete()
		# calculate_similar_artists(transferencias, "similar-artists.tsv",
  #                             factors=50, regularization=0.01,
  #                             iterations=15,
  #                             exact=False, trees=20,
  #                             use_native=True,
  #                             dtype=numpy.float64)
		

		return HttpResponse('<h1>Connection done!</h1>', {})