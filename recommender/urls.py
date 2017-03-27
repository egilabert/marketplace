from django.conf.urls import url
from django.contrib import admin

from .views import (SearchView,
                    HomeView,
                    ClientView,
                    ProviderView,
                    EmpresaDetailView,
                    OpportunityClientsView,
                    OpportunityProviderView)
                    
urlpatterns = [
    url(r'^$', HomeView, name='home'),
    url(r'^search/$', SearchView, name='search'),
    url(r'^clients/$', ClientView, name='clients'),
    url(r'^(?P<pk>\d+)/$', EmpresaDetailView, name='detail'),
    url(r'^providers/$', ProviderView, name='providers'),
    url(r'^client_oportunities/$', OpportunityClientsView, name='client_opportunities'),
    url(r'^provider_oportunities/$', OpportunityProviderView, name='provider_opportunities'),
]