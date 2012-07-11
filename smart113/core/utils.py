from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

class Tab(object):

    def __init__(self, name, address, is_active):
        self.name = name.split("-", 1)[1]
        self.address = address
        self.is_active = is_active

def get_tabs(request):
    tabs = []
    tabs.append(Tab(_('Basic'), reverse('profile-key')))
    tabs.append(Tab(_('Basic'), reverse('profile-physical')))

    user = request.user
    if user.profile.sight:
        tabs.append(Tab(_('Sight'), ""))
    if user.profile.hearing:
        tabs.append(Tab(_('Hearing'), ""))

    return tabs
