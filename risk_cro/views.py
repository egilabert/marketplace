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
			rater.patrimonio = form.cleaned_data['patrimonio']
			rater.activo_corriente = form.cleaned_data['activo_corriente']
			rater.activo_no_corriente = form.cleaned_data['activo_no_corriente']
			rater.pasivo_corriente = form.cleaned_data['pasivo_corriente']
			rater.pasivo_no_corriente = form.cleaned_data['pasivo_no_corriente']
			rater.importe_neto_cifra_negocio = form.cleaned_data['importe_neto_cifra_negocio']
			rater.gastos_financieros = form.cleaned_data['gastos_financieros']
			rater.resultados_antes_impuestos = form.cleaned_data['resultados_antes_impuestos']
			rater.save()
			context = {
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