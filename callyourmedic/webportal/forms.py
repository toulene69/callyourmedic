__author__ = 'apoorv'

from django import forms
from models import WebGroup, WebUser
from hospitals.models import Hospital, Department

class PortalUserLoginForm(forms.Form):
    org_identifier = forms.CharField(label = 'Org Identifier')
    user_name = forms.EmailField(label = 'Email ID')
    password  = forms.CharField(label = 'Password', widget = forms.PasswordInput)

class PortalUserGroupCreationForm(forms.ModelForm):
    class Meta:
        model = WebGroup
        exclude = ('grp_org_id',)

class PortalUserCreationForm(forms.ModelForm):
    def __init__(self,org_id,*args,**kwargs):
        super (PortalUserCreationForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['usr_group'].queryset = WebGroup.objects.filter(grp_org_id=org_id)

    class Meta:
        model = WebUser
        exclude = ('usr_password','usr_org',)


class PortalHospitalCreationForm(forms.ModelForm):

    class Meta:
        model = Hospital
        exclude = ('hospital_org','hospital_date_left','hospital_date_joined','hospital_status','hospital_address',)

class PortalHospitalSelectionForm(forms.Form):
    # choices = orgs = forms.ModelChoiceField(queryset=Hospital.objects.all(),empty_label="Select Hospital")
    QS_CHOICES = []
    choices = forms.ChoiceField(choices=QS_CHOICES)

    def __init__(self,org_id, *args, **kwargs):
        super(PortalHospitalSelectionForm, self).__init__(*args, **kwargs)
        self.QS_CHOICES = hospitalChoices(org_id)
        self.fields['choices'].choices = [('', 'Select a Hospital|Branch Code')] + list(hospitalChoices(org_id))


def hospitalChoices(org_id):
    choices = []
    hospitals = Hospital.objects.filter(hospital_org__exact = org_id)
    for hospital in hospitals:
        choice = (hospital.hospital_id , hospital.hospital_name + '|' + hospital.hospital_branch_code)
        choices.append(choice)
    return choices


class PortalDepartemntCreationForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PortalDepartemntCreationForm,self).__init__(*args,**kwargs)
        self.fields['department_description'] = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Department
        exclude = ('department_org','department_date_added',)

