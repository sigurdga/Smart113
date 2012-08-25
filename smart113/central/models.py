from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from smart113.core.models import UserProfile

class Search(models.Model):

    user = models.ForeignKey(User, null=True)
    from_backend = models.BooleanField(_('from backend'), default=False)
    query = models.CharField(max_length=100)
    datetime = models.DateTimeField(_('time'), auto_now_add=True)

    def __unicode__(self):
        return self.query

    class Meta:
        ordering = ['-datetime']

class SmartURL(models.Model):

    profile = models.ForeignKey(UserProfile)
    user = models.ForeignKey(User)
    used = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=36)

    def __unicode__(self):
        return "%s: %s" % (self.user.name, self.profile.user.name)

    class Meta:
        ordering = ['-used']
