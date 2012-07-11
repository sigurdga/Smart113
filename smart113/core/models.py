# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

GENDER_CHOICES = (
        (1, _('Female')),
        (2, _('Male')),
        (3, _('Other')),
        )

SIGHT_CHOICES = (
        #(1, _('Good')),
        (2, _('Glasses')),
        (3, _('Contact lenses')),
        (4, _('Partial blindness')),
        (5, _('Complete blindness')),
        )

HEARING_CHOICES = (
        #(1, _('Good')),
        (2, _('Nedsatt hearing')),
        (3, _('Needs device')),
        (4, _('Deaf')),
        )

SPEAKING_CHOICES = (
        #(1, _('Good')),
        (2, _('Some problems')),
        (3, _('Mute')),
        )

MOBILITY_CHOICES = (
        #(1, _('Working arms and legs')),
        (2, _('Reduced mobility')),
        )

ALLERGIES_CHOICES = (
        #(1, _('No known allergies')),
        (2, _('Some allergies')),
        )


class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

class Phone(models.Model):
    number = models.CharField(_('phone number'), max_length=20)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    # general information
    primary_language = models.ForeignKey(Language, null=True, blank=True, verbose_name=_('primary language'))
    birth_date = models.DateField(_('date of birth'), blank=True, null=True)
    gender = models.SmallIntegerField(_('gender'), choices=GENDER_CHOICES, null=True, blank=True)
    phones = models.ManyToManyField(Phone, blank=True)

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

    # key disabilities
    sight = models.SmallIntegerField(_('sight'), choices=SIGHT_CHOICES, null=True, blank=True)
    hearing = models.SmallIntegerField(_('hearing'), choices=HEARING_CHOICES, null=True, blank=True)
    speaking = models.SmallIntegerField(_('speaking'), choices=SPEAKING_CHOICES, null=True, blank=True)
    mobility = models.SmallIntegerField(_('mobility'), choices=MOBILITY_CHOICES, null=True, blank=True)
    allergies = models.SmallIntegerField(_('allergies'), choices=ALLERGIES_CHOICES, null=True, blank=True)

    # emergency
    amputation = models.NullBooleanField(_('amputation'), null=True)
    blind = models.NullBooleanField(_('blind'), null=True)
    cognitive = models.NullBooleanField(_('cognitive impairment'), null=True)
    stationary = models.NullBooleanField(_('stationary'), null=True)
    wheelchair = models.NullBooleanField(_('using wheelchair'), null=True)
    deaf = models.NullBooleanField(_('deaf'), null=True)
    #hearing = models.NullBooleanField(_('hearing impairment'), null=True)
    #mobility = models.NullBooleanField(_('reduced mobility'), null=True)
    mute = models.NullBooleanField(_('mute'), null=True)
    life_support = models.NullBooleanField(_('on life support'), null=True)
    walker = models.NullBooleanField(_('needs walker'), null=True)
    oxygen = models.NullBooleanField(_('needs oxygen'), null=True)

    class Meta:
        verbose_name, verbose_name_plural = _('profile'), _('profiles')

    def __unicode__(self):
        return self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.name = property(lambda u: u.get_full_name() or u.username)
