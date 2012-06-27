from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

GENDER_CHOICES = (
        (1, _('Female')),
        (2, _('Male')),
        (3, _('Other')),
        )

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

class Phone(models.Model):
    number = models.CharField(_('phone number'), max_length=20)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # key information
    primary_language = models.ForeignKey(Language, null=True, blank=True, verbose_name=_('primary language'))
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    gender = models.SmallIntegerField(_('gender'), choices=GENDER_CHOICES, null=True, blank=True)
    phones = models.ManyToManyField(Phone)

    # contact
    street_address = models.CharField(_('street_address'), max_length=60, blank=True)
    postcode = models.CharField(_('postcode'), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=30, blank=True)

    # physical
    hair_color = models.CharField(_('hair color'), max_length=20, blank=True)
    eye_color = models.CharField(_('eye color'), max_length=20, blank=True)
    weight = models.SmallIntegerField(_('weight'), null=True, blank=True)
    height = models.SmallIntegerField(_('height'), null=True, blank=True, help_text=_('in centimeters'))
    image = models.ImageField(_('image'), upload_to='pictures/', null=True, blank=True)
    extra = models.TextField(_('more'), null=True, blank=True)

    class Meta:
        verbose_name, verbose_name_plural = _('profile'), _('profiles')

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.name = property(lambda u: u.get_full_name() or u.username)
