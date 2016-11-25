from django.contrib import admin

# Register your models here.
from .models import Empresa, Transfer, RecommendedClients

class EmpresaAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "name", "sector", "cnae","territorial", "creation_date","updated_at"]
	list_display_links = ["name","updated_at"]
	list_filter = ["sector", "territorial"]
	list_editable = []
	search_fields = ["name", "territorial"]

	class Meta:
		model = Empresa

admin.site.register(Transfer)
admin.site.register(RecommendedClients)
admin.site.register(Empresa, EmpresaAdmin)