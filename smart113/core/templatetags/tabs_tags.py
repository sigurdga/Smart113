from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

register = template.Library()

from smart113.core.utils import get_tabs

class Tab(object):

    def __init__(self, name, address, path):
        self.name = name
        self.address = address
        self.is_active = path == address

@register.assignment_tag(takes_context=True)
def get_tabs(context):
    request = context['request']

    path = request.path_info
    user = request.user

    tabs = []
    tabs.append(Tab(_('Basic'), reverse('profile-basic'), path))
    tabs.append(Tab(_('Phone numbers'), reverse('profile-phone-list'), path))
    tabs.append(Tab(_('Physical'), reverse('profile-physical'), path))
    tabs.append(Tab(_('Key'), reverse('profile-key'), path))

    if user.profile.sight:
        tabs.append(Tab(_('Sight'), reverse('profile-sight'), path))
    if user.profile.hearing:
        tabs.append(Tab(_('Hearing'), reverse('profile-hearing'), path))
    if user.profile.hearing:
        tabs.append(Tab(_('Mobility'), reverse('profile-mobility'), path))
    if user.profile.hearing:
        tabs.append(Tab(_('Allergies'), reverse('profile-allergies'), path))

    return tabs
