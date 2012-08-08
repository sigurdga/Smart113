from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404

import urllib2
import json
from uuid import uuid4

from smart113.core.models import UserProfile, Phone, Relationship
from smart113.core.forms import *

class ProfileRelationshipCreateView(CreateView):
    model = UserProfile
    form_class = ProfileRelationForm
    template_name = "core/relation_form.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileRelationshipCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = User()
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.username = str(uuid4())[:30]
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.save()

        self.request.user.profile.add_relationship(profile, form.cleaned_data['relation'])

        return HttpResponseRedirect(reverse('relation-basic', kwargs={'pk': user.profile.id}))

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

class RelationDetailView(ProfileDetailView):

    def get_object(self):
        relationship = self.request.user.profile.get_all_relationships().filter(pk=self.kwargs.get('pk'))
        if relationship:
            return relationship[0]
        else:
            raise Http404()

class RelationBasicDetailView(RelationDetailView):
    template_name = "core/userprofile_basic_detail.html"

class RelationPhysicalDetailView(RelationDetailView):
    template_name = "core/userprofile_physical_detail.html"

class RelationKeyDetailView(RelationDetailView):
    template_name = "core/userprofile_key_detail.html"

class RelationSightDetailView(RelationDetailView):
    template_name = "core/userprofile_sight_detail.html"

class RelationHearingDetailView(RelationDetailView):
    template_name = "core/userprofile_hearing_detail.html"

class RelationMobilityDetailView(RelationDetailView):
    template_name = "core/userprofile_mobility_detail.html"

class RelationAllergiesDetailView(RelationDetailView):
    template_name = "core/userprofile_allergies_detail.html"

class ProfilePhoneListView(ListView):
    model = Phone

    def get_queryset(self):
        return super(ProfilePhoneListView, self).get_queryset().filter(userprofile=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super(ProfilePhoneListView, self).get_context_data(**kwargs)
        context['userprofile'] = self.request.user.profile
        return context

class RelationPhoneListView(ProfilePhoneListView):
    def get_queryset(self):
        relationships = self.request.user.profile.get_all_relationships().filter(pk=self.kwargs.get('pk'))
        if relationships:
            userprofile = relationships[0]
            return super(RelationPhoneListView, self).get_queryset().filter(userprofile=userprofile)
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ProfilePhoneListView, self).get_context_data(**kwargs)
        relationships = self.request.user.profile.get_all_relationships().filter(pk=self.kwargs.get('pk'))
        if relationships:
            context['userprofile'] = relationships[0]
        return context


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

class ProfileRelationshipListView(ListView):
    model = Relationship
    template_name = "core/relationship_list.html"

    def get_queryset(self):
        return Relationship.objects.filter(from_person=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super(ProfileRelationshipListView, self).get_context_data(**kwargs)
        context['userprofile'] = self.request.user.profile
        return context

class ProfileRelationshipDeleteView(DeleteView):
    model = Relationship
    success_url = lazy(reverse, str)("profile-relation-list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # TODO: Delete when no relations in either directions exist
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileRelationshipDeleteView, self).dispatch(*args, **kwargs)

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

class RelationUpdateView(ProfileUpdateView):

    def get_object(self):
        relationship = self.request.user.profile.get_all_relationships().filter(pk=self.kwargs.get('pk'))
        if relationship:
            return relationship[0]
        else:
            raise Http404()

class RelationBasicUpdateView(RelationUpdateView):
    form_class = ProfileBasicForm

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
        return HttpResponseRedirect(reverse('relation-basic', kwargs={'pk': self.object.pk}))

class RelationPhysicalUpdateView(RelationUpdateView):
    form_class = ProfilePhysicalForm

    def get_success_url(self):
        return reverse('relation-physical', kwargs={'pk': self.object.pk})

class RelationKeyUpdateView(RelationUpdateView):
    form_class = ProfileKeyForm

    def get_success_url(self):
        return reverse('relation-key', kwargs={'pk': self.object.pk})

class RelationSightUpdateView(RelationUpdateView):
    form_class = ProfileSightForm

    def get_success_url(self):
        return reverse('relation-sight', kwargs={'pk': self.object.pk})

class RelationHearingUpdateView(RelationUpdateView):
    form_class = ProfileHearingForm

    def get_success_url(self):
        return reverse('relation-hearing', kwargs={'pk': self.object.pk})

class RelationMobilityUpdateView(RelationUpdateView):
    form_class = ProfileMobilityForm

    def get_success_url(self):
        return reverse('relation-mobility', kwargs={'pk': self.object.pk})

class RelationAllergiesUpdateView(RelationUpdateView):
    form_class = ProfileAllergiesForm

    def get_success_url(self):
        return reverse('relation-allergies', kwargs={'pk': self.object.pk})

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
