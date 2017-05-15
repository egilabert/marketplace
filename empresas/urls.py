from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView, 
                    EmpresaDetailView,
                    InformeView,
                    DebugView,
                    # DataGenerator, 
                    ClientView, 
                    TransferListView, 
                    TransferDetailView, 
                    TrasferCreateView, 
                    CommercialClientsRecommendationsView2,
                    CommercialProvidersRecommendationsView2,
                    CommercialClientsRecommendationsView,
                    CommercialProvidersRecommendationsView,
                    FinancialRiskRecommendationsView,
                    ClientRiskRecommendationsView,
                    ProviderRiskRecommendationsView,
                    ProviderView,
                    EmpresasCreate,
                    ProductosCreate,
                    EstadosCreate,
                    CirbeCreate,
                    TranfersCreate,
                    ContentBasedCreate,
                    RecommendationsCreate,
                    OpportunityClientsView,
                    OpportunityProviderView,
                    FAQView,
                    SearchView,
                    IntroView,
                    SwitchView,
                    SummaryView,
                    get_data_mekko,
                    FinancialRiskRecommendationsView2,
                    MarketRiskRecommendationsView)

urlpatterns = [

    url(r'^intro/$', IntroView, name='empresas_intro'),
    url(r'^summary/$', SummaryView, name='summary'),
    url(r'^recommendations/clients$', CommercialClientsRecommendationsView2, name='recommendations_clients2'),
    url(r'^recommendations/providers$', CommercialProvidersRecommendationsView2, name='recommendations_providers2'),
    url(r'^recommendations/financial$', FinancialRiskRecommendationsView2, name='recommendations_financial2'),
    url(r'^get_data_mekko/$', get_data_mekko, name='get_data_mekko'),
    url(r'^$', HomeView, name='empresas_home'),
    #url(r'^create/$', EmpresaDetailView, name='empresa_create'),
    url(r'^(?P<pk>\d+)/$', EmpresaDetailView, name='detail'),
    url(r'^(?P<pk>\d+)/switch/$', SwitchView, name='switch'),
    url(r'^empresas/client_opportunities/$', OpportunityClientsView, name='client_opportunities'),
    url(r'^empresas/provider_opportunities/$', OpportunityProviderView, name='provider_opportunities'),
    #url(r'^update/$', EmpresaDetailView, name='empresa_update'),
    #url(r'^delete/$', EmpresaDetailView, name='empresa_delete'),
    url(r'^empresa/(?P<empresa_id>[0-9]+)/transfer_create/$', TrasferCreateView, name='transfer_create'),
    url(r'^faq/$', FAQView, name='faq'),
    
    url(r'^debug_recomendaciones/$', DebugView, name='debug'),
    url(r'^recomendaciones/$', InformeView, name='informe'),
    url(r'^search/$', SearchView, name='search'),
    url(r'^clients/$', ClientView, name='clients'),
    url(r'^providers/$', ProviderView, name='providers'),
    url(r'^recommendations/$', CommercialClientsRecommendationsView, name='recommendations'),
    url(r'^recommendations/providers/$', CommercialProvidersRecommendationsView, name='recommendations_providers'),
    url(r'^recommendations/risk/financial$', FinancialRiskRecommendationsView, name='recommendations_financial_risk'),
    url(r'^recommendations/risk/client$', ClientRiskRecommendationsView, name='recommendations_client_risk'),
    url(r'^recommendations/risk/market$', MarketRiskRecommendationsView, name='risk_market'),
    url(r'^recommendations/risk/provider$', ProviderRiskRecommendationsView, name='recommendations_provider_risk'),
    url(r'^transfers/$', TransferListView, name='transfer_list'),
    url(r'^transfers/(?P<transfer_id>[0-9]+)/$', TransferDetailView, name='transfer_detail'),

    # url(r'^generatedata/$', DataGenerator.as_view(), name='generate_empreses'),
    url(r'^generatedata/empresas/$', EmpresasCreate, name='empresas_create'),
    url(r'^generatedata/content_based/$', ContentBasedCreate, name='content_based_create'),
    url(r'^generatedata/productos/$', ProductosCreate, name='productos_create'),
    url(r'^generatedata/estados/$', EstadosCreate, name='estados_create'),
    url(r'^generatedata/transfers/$', TranfersCreate, name='transfers_create'),
    url(r'^generatedata/recommendations/$', RecommendationsCreate, name='recommedations_create'),
    url(r'^generatedata/cirbe/$', CirbeCreate, name='cirbe_create'),
]