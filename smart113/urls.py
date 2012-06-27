from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import logout
from django.contrib import admin
admin.autodiscover()

from smart113.views import HomeView

urlpatterns = patterns('',
        url(r'^$', HomeView.as_view(), name='home'),
        url(r'', include('social_auth.urls')),
        url(r'^logout/$', logout, name='auth_logout', kwargs={'next_page': '/'}),
)

if settings.DEVELOPMENT_MODE:
    import os

    urlpatterns += patterns('',
            (r'^files/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')}),
            )
