from django.contrib import admin

# Register your models here.
from .models import Empresa, Transfer, RecommendedClients, EstadosFinancieros, Productos, RecommendedProviders

class EmpresaAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "name", "sector", "cnae","territorial", "creation_date","updated_at"]
	list_display_links = ["name","updated_at"]
	list_filter = ["sector", "territorial"]
	list_editable = []
	search_fields = ["name", "territorial"]

	class Meta:
		model = Empresa

class EstadosFinancierosAdmin(admin.ModelAdmin):

	list_display = ["__unicode__", "empresa", "fecha_balance", "ventas","ebitda", "resultado_explotacion","created_at"]
	list_display_links = ["empresa","created_at"]
	list_filter = ["empresa", "fecha_balance"]
	list_editable = []
	search_fields = ["empresa", "fecha_balance"]

	class Meta:
		model = EstadosFinancieros

admin.site.register(EstadosFinancieros, EstadosFinancierosAdmin)
admin.site.register(Transfer)
admin.site.register(Productos)
admin.site.register(RecommendedClients)
admin.site.register(RecommendedProviders)
admin.site.register(Empresa, EmpresaAdmin)