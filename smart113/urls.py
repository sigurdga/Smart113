from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from smart113.views import HomeView

urlpatterns = patterns('',
        url(r'^$', HomeView.as_view(), name='home'),
)

if settings.DEVELOPMENT_MODE:
    import os

    urlpatterns += patterns('',
            (r'^files/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')}),
            )
