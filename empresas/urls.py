from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView, EmpresaDetailView, DataGenerator, ClientsView, TransferListView, TransferDetailView, TrasferCreateView, EmpresasListView)

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='empresas_home'),
    url(r'^list/$', EmpresasListView, name='empresas_list'),

    url(r'^generatedata/$', DataGenerator.as_view(), name='generate_empreses'),
    url(r'^clients/$', ClientsView.as_view(), name='clients'),
    #url(r'^providers/$', ProvidersView.as_view(), name='providers'),
    #url(r'^recommendations/$', RecommendationsView.as_view(), name='recommendations'),
    url(r'^empresa/(?P<empresa_id>[0-9]+)/$', EmpresaDetailView, name='empresa_detail'),
    url(r'^transfers/$', TransferListView, name='transfer_list'),
    url(r'^transfers/(?P<transfer_id>[0-9]+)/$', TransferDetailView, name='transfer_detail'),
    url(r'^empresa/(?P<empresa_id>[0-9]+)/transfer_create/$', TrasferCreateView, name='transfer_create'),
]