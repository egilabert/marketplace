"""marketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from empresas import views
from risk_cro import views
from business.views import LandingView, AppsView, TestView
from allauth.account.views import LoginView, SignupView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'), #views.home
    url(r'^admin/', admin.site.urls),
    url(r'^test/$', TestView),
    url(r'^pillstore/', AppsView.as_view(), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^empresas/', include('empresas.urls', namespace='empresas')),
    url(r'^cro/', include('risk_cro.urls', namespace='risk_cro')),
    url(r'^recommender/', include('recommender.urls', namespace='recommender')),
    url(r'^lcx/', include('LCX.urls', namespace='lcx')),
    url(r'^bidloan/', include('bidloan.urls', namespace='bidloan')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
