from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from smart113.core.views import *

urlpatterns = patterns('',
        url(r'^b$', ProfileBasicDetailView.as_view(), name="profile-basic"),
        url(r'^ph$', ProfilePhysicalDetailView.as_view(), name="profile-physical"),
        url(r'^k$', ProfileKeyDetailView.as_view(), name="profile-key"),
        url(r'^s$', ProfileSightDetailView.as_view(), name="profile-sight"),
        url(r'^h$', ProfileHearingDetailView.as_view(), name="profile-hearing"),
        url(r'^m$', ProfileMobilityDetailView.as_view(), name="profile-mobility"),
        url(r'^a$', ProfileAllergiesDetailView.as_view(), name="profile-allergies"),
        url(r'^e$', ProfileEmergencyDetailView.as_view(), name="profile-emergency"),
        url(r'^b/e$', ProfileBasicUpdateView.as_view(), name="update-basic"),
        url(r'^ph/e$', ProfilePhysicalUpdateView.as_view(), name="update-physical"),
        url(r'^k/e$', ProfileKeyUpdateView.as_view(), name="update-key"),
        url(r'^s/e$', ProfileSightUpdateView.as_view(), name="update-sight"),
        url(r'^h/e$', ProfileHearingUpdateView.as_view(), name="update-hearing"),
        url(r'^m/e$', ProfileMobilityUpdateView.as_view(), name="update-mobility"),
        url(r'^a/e$', ProfileAllergiesUpdateView.as_view(), name="update-allergies"),
        url(r'^e/e$', ProfileEmergencyUpdateView.as_view(), name="update-emergency"),
)
