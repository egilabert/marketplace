from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from empresas.models import Empresa
from .models import Rating
from .forms import RatingForm
import json

"""-------------------------------------------------------"""
"""				EMPRESAS VIEWS 							  """
"""-------------------------------------------------------"""

@login_required
def HomeView(request):
	try:
		del request.session['company']
		del request.session['recommended_clients_page']
	except:
		pass
	request.session.modified = True
	queryset = Empresa.objects.all()
	if request.session.get('company') is None:
		company = 990 #1492 #randint(0, queryset.count() - 1) # # ## 865 865-1 
		request.session['company'] = company
	else:
		company_id = request.session.get('company')
		company = Empresa.objects.filter(pk=company_id).first()
	return render(request, "cro_home.html", {'company': queryset[company-1], 'menu': False})

@login_required
def CreditRaterView(request):
	try:
		del request.session['company']
		del request.session['recommended_clients_page']
	except:
		pass
	request.session.modified = True
	queryset = Empresa.objects.all()
	if request.session.get('company') is None:
		company = 990 #1492 #randint(0, queryset.count() - 1) # # ## 865 865-1 
		request.session['company'] = company
	else:
		company_id = request.session.get('company')
		company = Empresa.objects.filter(pk=company_id).first()
	form = RatingForm()
	context = {
		'company': queryset[company-1], 
		'menu': False,
		'form': form
	}
	return render(request, "credit_risk.html", context)

@login_required
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