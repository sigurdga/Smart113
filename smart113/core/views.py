from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.http import HttpResponse, HttpResponseRedirect

import urllib2
import json

from smart113.core.models import UserProfile, Phone
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

class ProfilePhoneListView(ListView):
    model = Phone

    def get_queryset(self):
        return super(ProfilePhoneListView, self).get_queryset().filter(userprofile=self.request.user.profile)

class ProfilePhoneCreateView(CreateView):
    model = Phone
    success_url = lazy(reverse, str)("profile-phone-list")

    def form_valid(self, form):
        phone = form.save(commit=False)
        self.object, created = Phone.objects.get_or_create(number=phone.number)
        self.request.user.profile.phones.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfilePhoneCreateView, self).dispatch(*args, **kwargs)

class ProfilePhoneDeleteView(DeleteView):
    model = Phone
    success_url = lazy(reverse, str)("profile-phone-list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.user.profile.phones.remove(self.object)
        if not self.object.userprofile_set.all():
            self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfilePhoneDeleteView, self).dispatch(*args, **kwargs)

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

    def get_initial(self):
        initial = {}
        user = self.object.user
        if user.first_name:
            initial['first_name'] = user.first_name
        if user.last_name:
            initial['last_name'] = user.last_name
        #if user.username:
            #initial['username'] = user.username
        return initial

    def form_valid(self, form):
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        #self.object.user.username = form.cleaned_data['username']
        self.object.user.save()
        return HttpResponseRedirect(self.get_success_url())

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
