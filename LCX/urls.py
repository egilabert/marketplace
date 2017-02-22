from django.conf.urls import url
from django.contrib import admin

from .views import (HomeView,
					SegmentosView)

urlpatterns = [
    url(r'^$', HomeView, name='home'),
    url(r'^segmentos/$', SegmentosView, name='segmentos'),
]