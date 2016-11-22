from django.conf.urls import url
from django.contrib import admin

from .views import HomeView, DetailView

urlpatterns = [
    #url(r'^create/$', views.post_create, name='create'),
    url(r'^$', HomeView.as_view(), name='empresas_home'),
    url(r'^options/$', DetailView.as_view(), name='options'),
    
    #url(r'^(?P<id>[d]+)/$', DetailView.as_view(), name='detail'),
    #url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    #url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
]