from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
# Create your views here.

import allauth.account.forms as forms

class LandingView(View):
	def get(self, request, *args, **kwargs):
		form = forms.LoginForm()
		form_signup = forms.SignupForm()
		print ""
		print(form)
		print ""
		return render(request, "landing.html", {'form': form, 'form_signup': form_signup})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')

class AppsView(View):
	def get(self, request, *args, **kwargs):

		return render(request, "home.html", {'title': "FinApp Store"})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')