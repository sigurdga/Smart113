from django.conf.urls import patterns, url

from smart113.core.views import *

urlpatterns = patterns('',
        url(r'^k$', ProfileKeyDetailView.as_view(), name="profile-key"),
        url(r'^ph$', ProfilePhysicalDetailView.as_view(), name="profile-physical"),
)
