from django.conf.urls import patterns, url

from smart113.central.views import *

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='central-home'),
    url(r'^p/(?P<pk>\d+)$', SmartURLRedirectView.as_view(), name='central-smarturl-redirect'),
    url(r'^p/(?P<slug>[-\w]+)$', SmartURLView.as_view(), name='central-smarturl-detail'),
    url(r'^search/(?P<number>\d+)$', PhoneListView.as_view(), name="central-phone-list"),
)
