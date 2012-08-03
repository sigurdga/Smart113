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

    tabs = []

    path = request.path_info
    user = request.user

    userprofile = context['userprofile']

    if userprofile == user.profile:
        tabs.append(Tab(_('Basic'), reverse('profile-basic'), path))
        tabs.append(Tab(_('Phone numbers'), reverse('profile-phone-list'), path))
        tabs.append(Tab(_('Physical'), reverse('profile-physical'), path))
        tabs.append(Tab(_('Key'), reverse('profile-key'), path))

        if user.profile.sight:
            tabs.append(Tab(_('Sight'), reverse('profile-sight'), path))
        if user.profile.hearing:
            tabs.append(Tab(_('Hearing'), reverse('profile-hearing'), path))
        #if user.profile.speaking:
            #tabs.append(Tab(_('Speaking'), reverse('profile-speaking'), path))
        if user.profile.mobility:
            tabs.append(Tab(_('Mobility'), reverse('profile-mobility'), path))
        if user.profile.allergies:
            tabs.append(Tab(_('Allergies'), reverse('profile-allergies'), path))

        tabs.append(Tab(_('Emergency contacts'), reverse('profile-relation-list'), path))

    else:
        user_id = userprofile.user.id
        tabs.append(Tab(_('Basic'), reverse('relation-basic', kwargs={'pk': user_id}), path))
        #tabs.append(Tab(_('Phone numbers'), reverse('relation-phone-list', kwargs={'pk': user_id}), path))
        tabs.append(Tab(_('Physical'), reverse('relation-physical', kwargs={'pk': user_id}), path))
        tabs.append(Tab(_('Key'), reverse('relation-key', kwargs={'pk': user_id}), path))

        if userprofile.sight:
            tabs.append(Tab(_('Sight'), reverse('relation-sight', kwargs={'pk': user_id}), path))
        if userprofile.hearing:
            tabs.append(Tab(_('Hearing'), reverse('relation-hearing', kwargs={'pk': user_id}), path))
        #if userprofile.speaking:
            #tabs.append(Tab(_('Speaking'), reverse('relation-speaking', kwargs={'pk': user_id}), path))
        if userprofile.mobility:
            tabs.append(Tab(_('Mobility'), reverse('relation-mobility', kwargs={'pk': user_id}), path))
        if userprofile.allergies:
            tabs.append(Tab(_('Allergies'), reverse('relation-allergies', kwargs={'pk': user_id}), path))

    return tabs
