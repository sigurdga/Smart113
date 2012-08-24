from django.views.generic import ListView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import ugettext as _

from datetime import datetime, timedelta

from smart113.core.models import UserProfile, Phone
from smart113.central.models import Search

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


