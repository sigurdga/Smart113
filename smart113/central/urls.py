from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from smart113.central.views import *

urlpatterns = patterns('',
        url(r'^search/(?P<number>\d+)$', PhoneListView.as_view(), name="central-phone-list"),
)
