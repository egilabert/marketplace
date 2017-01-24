from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView,
					CreditRaterView,
					RaterView)

urlpatterns = [
    url(r'^$', HomeView, name='cro_home'),
    url(r'^creditrater/$', CreditRaterView, name='credit_risk'),
    url(r'^rating/$', RaterView, name='rater'),
]