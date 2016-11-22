from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
# Create your views here.

import allauth.account.forms as forms

class LandingView(View):
	def get(self, request, *args, **kwargs):
		form = forms.LoginForm()
		print(form)
		return render(request, "landing.html", {'form': form})

	def post(self, request, *args, **kwargs):
		return HttpResponse('<h1>Home POST page</h1>')