from django.views.generic import ListView, DetailView, RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta
from uuid import uuid4

from smart113.core.models import UserProfile, Phone
from smart113.central.models import Search, SmartURL

class HomeView(ListView):
    template_name = "central/home.html"
    model = Search

    def get_queryset(self):
        time_ago = datetime.now() - timedelta(hours=6)
        return super(HomeView, self).get_queryset().filter(datetime__gt=time_ago)


class PhoneListView(ListView):

    model = Phone
    template_name = "central/phone_list.html"

    def get_queryset(self):
        number = self.kwargs.get('number')
        if len(number) >= 8:
            return super(PhoneListView, self).get_queryset().filter(number__endswith=number)
        else:
            messages.warning(self.request, _("That is not a phone number, make it longer"))
            return super(PhoneListView, self).get_queryset().none()

    def get_context_data(self, **kwargs):
        context = super(PhoneListView, self).get_context_data(**kwargs)
        context['number'] = self.kwargs.get('number')
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PhoneListView, self).dispatch(*args, **kwargs)

class SmartURLView(DetailView):

    model = SmartURL
    template_name = 'central/profile_full.html'

class SmartURLRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        profile = get_object_or_404(UserProfile, pk=pk)
        timeago = datetime.now() - timedelta(hours=2)
        try:
            smarturl = SmartURL.objects.filter(user=self.request.user, used__gt=timeago).first()
        except:
            smarturl = SmartURL()
            smarturl.slug = str(uuid4())
            smarturl.user = self.request.user
            smarturl.profile = profile

        smarturl.save() # should update timestamp

        return reverse('central-smarturl-detail', kwargs={'slug': smarturl.slug})
