from django import forms
from django.forms.extras.widgets import SelectDateWidget

import datetime

from smart113.core.models import UserProfile, RELATIONSHIP_CHOICES

def get_years():
    year = datetime.date.today().year
    return range(year, year-100, -1)

class ProfileRelationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    relation = forms.ChoiceField(RELATIONSHIP_CHOICES)
    same_address = forms.BooleanField(required=False)
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'relation', 'same_address']


class ProfileBasicForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'street_address', 'postcode', 'city', 'primary_language', 'birth_date', 'gender']
        widgets = {'birth_date': SelectDateWidget(years=get_years()) }

class ProfilePhysicalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender', 'hair_color', 'eye_color', 'weight', 'height', 'image', 'extra']

class ProfileKeyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['sight', 'hearing', 'speaking', 'mobility', 'allergies']

class ProfileSightForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['sight']

class ProfileHearingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['hearing']

class ProfileMobilityForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mobility']

class ProfileAllergiesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['allergies']

class ProfileEmergencyForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['amputation', 'blind', 'cognitive', 'stationary', 'wheelchair', 'walker', 'mobility', 'deaf', 'hearing', 'mute', 'life_support', 'oxygen']
