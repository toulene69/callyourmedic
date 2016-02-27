__author__ = 'apoorv'

from django import forms
from models import Group
from models import User
from organisations.models import Organisation
from hospitals.models import Hospital

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

class CYMOrgHospitalSelectionForm(forms.Form):

    QS_CHOICES = []
    hospitals = forms.ChoiceField(choices=QS_CHOICES)
    def __init__(self,org_id, *args, **kwargs):
        super(CYMOrgHospitalSelectionForm, self).__init__(*args, **kwargs)
        self.QS_CHOICES = hospitalChoices(org_id)
        self.fields['hospitals'].choices = [('', 'Select a Hospital|Branch Code')] + list(hospitalChoices(org_id))



def hospitalChoices(org_id):
    choices = []
    hospitals = Hospital.objects.filter(hospital_org__exact = org_id)
    for hospital in hospitals:
        choice = (hospital.hospital_id , hospital.hospital_name + '|' + hospital.hospital_branch_code)
        choices.append(choice)
    return choices