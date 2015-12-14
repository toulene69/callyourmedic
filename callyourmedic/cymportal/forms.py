__author__ = 'apoorv'

from django import forms
from models import Group
from models import User
from organisations.models import Organisation

class CYMUserLoginForm(forms.Form):
    user_name = forms.EmailField(label = 'Email ID')
    password  = forms.CharField(label = 'Password', widget = forms.PasswordInput)



class CYMUserGroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

class CYMUserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('usr_password',)


class CYMOrganisationCreationForm(forms.ModelForm):

    class Meta:
        model = Organisation
        exclude = ('org_address','org_identifier','org_date_joined','org_date_left','org_billing_id',)


class CYMOrganisationSelectionForm(forms.ModelForm):
    orgs = forms.ModelChoiceField(queryset=Organisation.objects.all(),empty_label="Select Organisation")
    class Meta:
        model = Organisation
        exclude = '__all__'
