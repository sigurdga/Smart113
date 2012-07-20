from django.views.generic import View, DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.http import HttpResponse

import urllib2
import json

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

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

class JSONView(JSONResponseMixin, View):
    pass

class ProxyView(JSONView):

    def get(self, request, *args, **kwargs):
        #if request.is_ajax():
        headers = { 'User-Agent' : 'StrekmannLocation/0.1' }
        url = 'http://open.mapquestapi.com/geocoding/v1/reverse?lat=%s&lng=%s' % (self.kwargs.get('lat'), self.kwargs.get('lon'))
        print url
        req = urllib2.Request(url, headers=headers)
        data = urllib2.urlopen(req).read()
        print data
        return self.render_to_response(data)

