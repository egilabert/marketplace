from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

@method_decorator(login_required, name='dispatch')
class HomeView(View):
	def get(self, request, *args, **kwargs):
		return render(request, "empresas_home.html", {})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')

# Create your views here.
def empreses_create(request):
	return HttpResponse("<h1>Create</h1>")

@method_decorator(login_required, name='dispatch')
class DetailView(View):
	def get(self, request, *args, **kwargs):
		return render(request, "market_option.html", {})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')

def empreses_update(request):
	return HttpResponse("<h1>Update</h1>")

def empreses_delete(request):
	return HttpResponse("<h1>Delete</h1>")
