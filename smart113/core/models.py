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

RELATIONSHIP_SIGNIFICANT_OTHER = 1
RELATIONSHIP_CHILD = 2
RELATIONSHIP_PARENT = 3
RELATIONSHIP_SIBLING = 4
RELATIONSHIP_GRANDCHILD = 5
RELATIONSHIP_GRANDPARENT = 6
RELATIONSHIP_PARENTINLAW = 11
RELATIONSHIP_NEIGHBOUR = 7
RELATIONSHIP_FRIEND = 8
RELATIONSHIP_COWORKER = 9
RELATIONSHIP_OTHER = 10
RELATIONSHIP_CHOICES = (
        (RELATIONSHIP_SIGNIFICANT_OTHER, _("Significant other")),
        (RELATIONSHIP_CHILD, _("Child")),
        (RELATIONSHIP_PARENT, _("Parent")),
        (RELATIONSHIP_SIBLING, _("Sibling")),
        (RELATIONSHIP_GRANDCHILD, _("Grandchild")),
        (RELATIONSHIP_GRANDPARENT, _("Grandparent")),
        (RELATIONSHIP_PARENTINLAW, _("Parent in law")),
        (RELATIONSHIP_NEIGHBOUR, _("Neighbour")),
        (RELATIONSHIP_FRIEND, _("Friend")),
        (RELATIONSHIP_COWORKER, _("Co-worker")),
        (RELATIONSHIP_OTHER, _("Other")),
        )

class Relationship(models.Model):
    from_person = models.ForeignKey('UserProfile', related_name='from_people')
    to_person = models.ForeignKey('UserProfile', related_name='to_people')
    relation = models.IntegerField(choices=RELATIONSHIP_CHOICES)
    same_address = models.NullBooleanField(_("Living at your address"), null=True)

    def __unicode__(self):
        return u"%s %s" % (self.from_person, self.to_person)

class Language(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

class Phone(models.Model):
    number = models.CharField(_('phone number'), max_length=20)

    def __unicode__(self):
        return self.number

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    relationships = models.ManyToManyField('self', through='Relationship',
            symmetrical=False,
            related_name='related_to')

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

    def age(self):
        if self.birth_date:
            from datetime import date
            today = date.today()
            born = self.birth_date

            try:
                birthday = born.replace(year=today.year)
            except ValueError:
                # raised when birth date is February 29 and the current year is not a leap year
                birthday = born.replace(year=today.year, day=born.day-1)

            if birthday > today:
                return today.year - born.year - 1
            else:
                return today.year - born.year

    def add_relationship(self, person, relation):
        relationship, created = Relationship.objects.get_or_create(
                from_person=self,
                to_person=person,
                relation=relation)
        return relationship

    def remove_relationship(self, person, relation):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            relation=relation).delete()

    def get_all_relationships(self):
        a = self.relationships.filter(
            to_people__from_person=self,
            )
        print a
        return a
    def get_relationships(self, relation, same_address=False):
        return self.relationships.filter(
            to_people__relation=relation,
            to_people__from_person=self,
            #same_address=same_address,
            )

    def get_related_to(self, relation, same_address=False):
        return self.related_to.filter(
            from_people__relation=relation,
            from_people__to_person=self,
            same_address=same_address)

    def get_significant_others(self):
        return self.get_relationships(RELATIONSHIP_SIGNIFICANT_OTHER)

    def get_children(self):
        return self.get_relationships(RELATIONSHIP_CHILD)

    def get_parents(self):
        return self.get_relationships(RELATIONSHIP_PARENT)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.name = property(lambda u: u.get_full_name() or u.username)
