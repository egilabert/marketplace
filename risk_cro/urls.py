from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView,
					CreditRaterView,
					RaterView,
                    EmpresaDetailView,
                    SearchView,
                    SummaryView,
                    MarketRiskRecommendationsView,
                    CommercialClientsRecommendationsView,
                    CommercialProvidersRecommendationsView,
                    FinancialRiskRecommendationsView)

urlpatterns = [
    url(r'^$', HomeView, name='cro_home'),
    url(r'^search/$', SearchView, name='search'),
    url(r'^summary/$', SummaryView, name='summary'),
    url(r'^(?P<pk>\d+)/$', EmpresaDetailView, name='detail'),
    url(r'^creditrater/$', CreditRaterView, name='credit_risk'),
    url(r'^rating/$', RaterView, name='rater'),
    url(r'^market_risk/$', MarketRiskRecommendationsView, name='market_risk'),
    url(r'^client_risk/$', CommercialClientsRecommendationsView, name='client_risk'),
    url(r'^provider_risk/$', CommercialProvidersRecommendationsView, name='provider_risk'),
    url(r'^financial_risk/$', FinancialRiskRecommendationsView, name='financial_risk'),
    
]