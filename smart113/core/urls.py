from django.conf.urls import patterns, url
from django.utils.translation import ugettext as _

from smart113.core.views import *

urlpatterns = patterns('',
        url(r'^$', ProfileDetailView.as_view(), name="profile-detail"),
        url(r'^p$', ProfilePhoneListView.as_view(), name="profile-phone-list"),
        url(r'^p/a$', ProfilePhoneCreateView.as_view(), name="profile-phone-create"),
        url(r'^p/d/(?P<pk>\d+)$', ProfilePhoneDeleteView.as_view(), name="profile-phone-delete"),

        url(r'^r$', ProfileRelationshipListView.as_view(), name="profile-relation-list"),
        url(r'^r/a$', ProfileRelationshipCreateView.as_view(), name="profile-relation-create"),
        url(r'^r/d/(?P<pk>\d+)$', ProfileRelationshipDeleteView.as_view(), name="profile-relation-delete"),

        url(r'^p/rel/(?P<pk>\d+)$', RelationPhoneListView.as_view(), name="relation-phone-list"),
        url(r'^b/rel/(?P<pk>\d+)$', RelationBasicDetailView.as_view(), name="relation-basic"),
        url(r'^ph/rel/(?P<pk>\d+)$', RelationPhysicalDetailView.as_view(), name="relation-physical"),
        url(r'^k/rel/(?P<pk>\d+)$', RelationKeyDetailView.as_view(), name="relation-key"),
        url(r'^s/rel/(?P<pk>\d+)$', RelationSightDetailView.as_view(), name="relation-sight"),
        url(r'^h/rel/(?P<pk>\d+)$', RelationHearingDetailView.as_view(), name="relation-hearing"),
        url(r'^m/rel/(?P<pk>\d+)$', RelationMobilityDetailView.as_view(), name="relation-mobility"),
        url(r'^a/rel/(?P<pk>\d+)$', RelationAllergiesDetailView.as_view(), name="relation-allergies"),
        # Update
        url(r'^b/rel/(?P<pk>\d+)/e$', RelationBasicUpdateView.as_view(), name="relation-basic-update"),
        url(r'^ph/rel/(?P<pk>\d+)/e$', RelationPhysicalUpdateView.as_view(), name="relation-physical-update"),
        url(r'^k/rel/(?P<pk>\d+)/e$', RelationKeyUpdateView.as_view(), name="relation-key-update"),
        url(r'^s/rel/(?P<pk>\d+)/e$', RelationSightUpdateView.as_view(), name="relation-sight-update"),
        url(r'^h/rel/(?P<pk>\d+)/e$', RelationHearingUpdateView.as_view(), name="relation-hearing-update"),
        url(r'^m/rel/(?P<pk>\d+)/e$', RelationMobilityUpdateView.as_view(), name="relation-mobility-update"),
        url(r'^a/rel/(?P<pk>\d+)/e$', RelationAllergiesUpdateView.as_view(), name="relation-allergies-update"),

        url(r'^b/e$', ProfileBasicUpdateView.as_view(), name="update-basic"),
        url(r'^ph/e$', ProfilePhysicalUpdateView.as_view(), name="update-physical"),
        url(r'^k/e$', ProfileKeyUpdateView.as_view(), name="update-key"),
        url(r'^s/e$', ProfileSightUpdateView.as_view(), name="update-sight"),
        url(r'^h/e$', ProfileHearingUpdateView.as_view(), name="update-hearing"),
        url(r'^m/e$', ProfileMobilityUpdateView.as_view(), name="update-mobility"),
        url(r'^a/e$', ProfileAllergiesUpdateView.as_view(), name="update-allergies"),
        url(r'^e/e$', ProfileEmergencyUpdateView.as_view(), name="update-emergency"),
)
