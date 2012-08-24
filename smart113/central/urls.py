from django.conf.urls import patterns, url

from smart113.central.views import *

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='central-home'),
    url(r'^search/(?P<number>\d+)$', PhoneListView.as_view(), name="central-phone-list"),
)
