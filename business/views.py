from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
# Create your views here.

import allauth.account.forms as forms

class LandingView(View):
	def get(self, request, *args, **kwargs):
		# form = forms.LoginForm()
		# form_signup = forms.SignupForm()
		return render(request, "landing.html", {})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')

class AppsView(View):
	def get(self, request, *args, **kwargs):
		return render(request, "home.html", {'title': "Our Pillstore"})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')

def TestView(request):
	context = {
		'title': "Grid Composition"}
	return render(request, 'test_cards.html', context)