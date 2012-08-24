from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Search(models.Model):

    user = models.ForeignKey(User, null=True)
    from_backend = models.BooleanField(_('from backend'), default=False)
    query = models.CharField(max_length=100)
    datetime = models.DateTimeField(_('time'), auto_now_add=True)

    def __unicode__(self):
        return self.query

    class Meta:
        ordering = ['-datetime']
