from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView, 
                    EmpresaDetailView, 
                    DataGenerator, 
                    ClientView, 
                    TransferListView, 
                    TransferDetailView, 
                    TrasferCreateView, 
                    EmpresasListView,
                    RecommendationsView,
                    ProviderView)

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='empresas_home'),
    url(r'^list/$', EmpresasListView, name='empresas_list'),
    url(r'^empresa/(?P<empresa_id>[0-9]+)/$', EmpresaDetailView, name='empresa_detail'),
    url(r'^empresa/(?P<empresa_id>[0-9]+)/transfer_create/$', TrasferCreateView, name='transfer_create'),
    
    url(r'^clients/$', ClientView, name='clients'),
    url(r'^providers/$', ProviderView, name='providers'),
    url(r'^recommendations/$', RecommendationsView, name='recommendations'),
    url(r'^transfers/$', TransferListView, name='transfer_list'),
    url(r'^transfers/(?P<transfer_id>[0-9]+)/$', TransferDetailView, name='transfer_detail'),
    url(r'^generatedata/$', DataGenerator.as_view(), name='generate_empreses'),

]