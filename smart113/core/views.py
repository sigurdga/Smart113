from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

from smart113.core.models import UserProfile
from smart113.core.forms import *

class ProfileDetailView(DetailView):
    model = UserProfile

    def get_object(self):
        return self.request.user.profile

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileDetailView, self).dispatch(*args, **kwargs)

class ProfileBasicDetailView(ProfileDetailView):
    template_name = "core/userprofile_basic_detail.html"

class ProfilePhysicalDetailView(ProfileDetailView):
    template_name = "core/userprofile_physical_detail.html"

class ProfileKeyDetailView(ProfileDetailView):
    template_name = "core/userprofile_key_detail.html"

class ProfileSightDetailView(ProfileDetailView):
    template_name = "core/userprofile_sight_detail.html"

class ProfileHearingDetailView(ProfileDetailView):
    template_name = "core/userprofile_hearing_detail.html"

class ProfileMobilityDetailView(ProfileDetailView):
    template_name = "core/userprofile_mobility_detail.html"

class ProfileAllergiesDetailView(ProfileDetailView):
    template_name = "core/userprofile_allergies_detail.html"

class ProfileEmergencyDetailView(ProfileDetailView):
    template_name = "core/userprofile_emergency_detail.html"

class ProfileUpdateView(UpdateView):
    model = UserProfile

    def get_object(self):
        return self.request.user.profile

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)


class ProfileBasicUpdateView(ProfileUpdateView):
    form_class = ProfileBasicForm
    success_url = lazy(reverse, str)("profile-basic")

class ProfilePhysicalUpdateView(ProfileUpdateView):
    form_class = ProfilePhysicalForm
    success_url = lazy(reverse, str)("profile-physical")

class ProfileKeyUpdateView(ProfileUpdateView):
    form_class = ProfileKeyForm
    success_url = lazy(reverse, str)("profile-key")

class ProfileSightUpdateView(ProfileUpdateView):
    form_class = ProfileSightForm
    success_url = lazy(reverse, str)("profile-sight")

class ProfileHearingUpdateView(ProfileUpdateView):
    form_class = ProfileHearingForm
    success_url = lazy(reverse, str)("profile-hearing")

class ProfileMobilityUpdateView(ProfileUpdateView):
    form_class = ProfileMobilityForm
    success_url = lazy(reverse, str)("profile-mobility")

class ProfileAllergiesUpdateView(ProfileUpdateView):
    form_class = ProfileAllergiesForm
    success_url = lazy(reverse, str)("profile-allergies")

class ProfileEmergencyUpdateView(ProfileUpdateView):
    form_class = ProfileEmergencyForm
    success_url = lazy(reverse, str)("profile-emergency")
