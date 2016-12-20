from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView, 
                    EmpresaDetailView, 
                    DataGenerator, 
                    ClientView, 
                    TransferListView, 
                    TransferDetailView, 
                    TrasferCreateView, 
                    CommercialClientsRecommendationsView,
                    CommercialProvidersRecommendationsView,
                    ProviderView,
                    EmpresasCreate,
                    ProductosCreate,
                    EstadosCreate,
                    TranfersCreate,
                    RecommendationsCreate,
                    OpportunityClientsView,
                    OpportunityProviderView)

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='empresas_home'),
    #url(r'^create/$', EmpresaDetailView, name='empresa_create'),
    url(r'^(?P<pk>\d+)/$', EmpresaDetailView, name='detail'),
    url(r'^empresas/client_opportunities/$', OpportunityClientsView, name='client_opportunities'),
    url(r'^empresas/provider_opportunities/$', OpportunityProviderView, name='provider_opportunities'),
    #url(r'^update/$', EmpresaDetailView, name='empresa_update'),
    #url(r'^delete/$', EmpresaDetailView, name='empresa_delete'),
    url(r'^empresa/(?P<empresa_id>[0-9]+)/transfer_create/$', TrasferCreateView, name='transfer_create'),
    
    url(r'^clients/$', ClientView, name='clients'),
    url(r'^providers/$', ProviderView, name='providers'),
    url(r'^recommendations/$', CommercialClientsRecommendationsView, name='recommendations'),
    url(r'^recommendations/providers/$', CommercialProvidersRecommendationsView, name='recommendations_providers'),
    url(r'^transfers/$', TransferListView, name='transfer_list'),
    url(r'^transfers/(?P<transfer_id>[0-9]+)/$', TransferDetailView, name='transfer_detail'),

    url(r'^generatedata/$', DataGenerator.as_view(), name='generate_empreses'),
    url(r'^generatedata/empresas/$', EmpresasCreate, name='empresas_create'),
    url(r'^generatedata/productos/$', ProductosCreate, name='productos_create'),
    url(r'^generatedata/estados/$', EstadosCreate, name='estados_create'),
    url(r'^generatedata/transfers/$', TranfersCreate, name='transfers_create'),
    url(r'^generatedata/recommendations/$', RecommendationsCreate, name='recommedations_create'),
    

]