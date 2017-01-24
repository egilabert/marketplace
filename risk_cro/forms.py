from django import forms

class RatingForm(forms.Form):
	sector = forms.CharField()
	name = forms.CharField(max_length=255)
	antiguedad = forms.CharField(max_length=255)
	patrimonio = forms.IntegerField()
	fondos_propios = forms.IntegerField()
	activo_corriente = forms.IntegerField()
	activo_no_corriente = forms.IntegerField()
	pasivo_corriente = forms.IntegerField()
	pasivo_no_corriente = forms.IntegerField()
	importe_neto_cifra_negocio = forms.IntegerField()
	gastos_financieros = forms.IntegerField()
	resultados_antes_impuestos = forms.IntegerField()