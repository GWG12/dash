from user.forms import UserRegistrationForm
from django.forms import HiddenInput
from django import forms
from user.models import Profile
from django.db import models


class SubscriptionRegistrationForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
    attrs={
        'data-openpay-card':"holder_name",
        'class': 'input is-large',
        'placeholder': 'Nombre'
    }))
    project_name = forms.CharField(widget=forms.TextInput(
    attrs={
        'class': 'input is-large',
        'placeholder': 'Nombre del Proyecto'
    }))
    class Meta:
        #fields = UserRegistrationForm.Meta.fields + ('name','company','address','cp','county','state')
        model = Profile
        fields = ('name','project_name')
