from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def empreses_create(request):
	return HttpResponse("<h1>Create</h1>")

def empreses_detail(request):
	return HttpResponse("<h1>Detail</h1>")

def home(request):
	return render(request, "home.html", {})

def empreses_update(request):
	return HttpResponse("<h1>Update</h1>")

def empreses_delete(request):
	return HttpResponse("<h1>Delete</h1>")
