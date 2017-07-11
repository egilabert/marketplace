from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="bidloan/landing.html")),
    url(r'^new_auction/$', TemplateView.as_view(template_name="bidloan/new_auction.html"), name="new_auction"),
    url(r'^dashboard/$', TemplateView.as_view(template_name="bidloan/dashboard.html"), name="dashboard"),
]