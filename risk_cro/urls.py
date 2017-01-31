from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView,
					CreditRaterView,
					RaterView,
					ClientRiskView,
					ClientRiskRecommendationsView,
					ProviderRiskRecommendationsView)

urlpatterns = [
    url(r'^$', HomeView, name='cro_home'),
    url(r'^creditrater/$', CreditRaterView, name='credit_risk'),
    url(r'^rating/$', RaterView, name='rater'),
    url(r'^client/$', ClientRiskView, name='client_risk'),
    url(r'^client/client/$', ClientRiskRecommendationsView, name='client_client_risk'),
    url(r'^client/provider/$', ProviderRiskRecommendationsView, name='client_provider_risk'),
]