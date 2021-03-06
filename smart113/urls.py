from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.views import login, logout
from django.contrib import admin
admin.autodiscover()

from smart113.views import HomeView

urlpatterns = patterns('',
        url(r'^$', HomeView.as_view(), name='home'),
        url(r'', include('social_auth.urls')),
        url(r'^c/', include('smart113.central.urls')),
        url(r'^profile/', include('smart113.core.urls')),
        url(r'^logout/$', logout, name='auth_logout', kwargs={'next_page': '/'}),
        url(r'^login/$', login, name='auth_login'),
        url(r'^admin/', include(admin.site.urls)),
)

if settings.DEVELOPMENT_MODE:
    import os

    urlpatterns += patterns('',
            (r'^files/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files')}),
            )
