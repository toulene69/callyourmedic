__author__ = 'apoorv'

from django import forms
from django.core.exceptions import ValidationError
from models import WebGroup, WebUser
from hospitals.models import Hospital, Department, HospitalSettings
from doctors.models import DoctorDetails, DoctorRegistration, DoctorSettings
from organisations.models import OrgSettings

class UploadFileForm(forms.Form):
    file = forms.FileField(required=False)

    def clean_file(self):
        file = self.cleaned_data.get('file', False)
        if file:
            if file._size > 1024 * 1024:
                raise ValidationError("Image file too large ( > 1mb )")
        return file

class PortalUserLoginForm(forms.Form):
    org_identifier = forms.CharField(label = 'Org Identifier')
    user_name = forms.EmailField(label = 'Email ID')
    password  = forms.CharField(label = 'Password', widget = forms.PasswordInput)

class PortalUserGroupCreationForm(forms.ModelForm):
    class Meta:
        model = WebGroup
        exclude = ('grp_org_id','is_super',)

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
        exclude = ('hospital_org','hospital_date_left','hospital_date_joined','hospital_status','hospital_address','hospital_settings',)

class PortalHospitalEditForm(forms.ModelForm):

    class Meta:
        model = Hospital
        exclude = ('hospital_id','hospital_org','hospital_date_left','hospital_settings','hospital_address','hospital_date_joined')

class PortalHospitalSelectionForm(forms.Form):
    # choices = orgs = forms.ModelChoiceField(queryset=Hospital.objects.all(),empty_label="Select Hospital")
    QS_CHOICES = []
    choices = forms.ChoiceField(choices=QS_CHOICES)

    def __init__(self,org_id, *args, **kwargs):
        super(PortalHospitalSelectionForm, self).__init__(*args, **kwargs)
        self.QS_CHOICES = hospitalChoices(org_id)
        self.fields['choices'].choices = [('', 'Select a Hospital|Branch Code')] + list(hospitalChoices(org_id))


class PortalDepartmentCreationForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PortalDepartmentCreationForm,self).__init__(*args,**kwargs)
        self.fields['department_description'] = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Department
        exclude = ('department_org','department_date_added',)


class PortalDoctorRegistrationForm(forms.ModelForm):
    HOSPITAL_CHOICES = []
    DEPT_CHOICES = []
    hospital_choice = forms.ChoiceField(choices=HOSPITAL_CHOICES)
    dept_choice = forms.ChoiceField(choices=DEPT_CHOICES)
    def __init__(self,org_id,*args,**kwargs):
        super (PortalDoctorRegistrationForm,self ).__init__(*args,**kwargs) # populates the post
        # self.fields['doctor_hospital'].queryset = Hospital.objects.filter(hospital_org__exact=org_id)
        # self.fields['doctor_department'].queryset = Department.objects.filter(department_org__exact = org_id)
        self.HOSPITAL_CHOICES = hospitalChoices(org_id)
        self.DEPT_CHOICES = departmentChoices(org_id)
        self.fields['hospital_choice'].choices = [('', 'Select a Hospital|Branch Code')] + list(hospitalChoices(org_id))
        self.fields['dept_choice'].choices = [('', 'Select a Department|Dept Code')] + list(departmentChoices(org_id))

    class Meta:
        model = DoctorRegistration
        fields = ('doctor_email',)

class PortalDoctorRegistrationEditForm(forms.ModelForm):
    HOSPITAL_CHOICES = []
    DEPT_CHOICES = []
    hospital_choice = forms.ChoiceField(choices=HOSPITAL_CHOICES)
    dept_choice = forms.ChoiceField(choices=DEPT_CHOICES)
    def __init__(self,org_id,*args,**kwargs):
        super (PortalDoctorRegistrationEditForm,self ).__init__(*args,**kwargs) # populates the post
        # self.fields['doctor_hospital'].queryset = Hospital.objects.filter(hospital_org__exact=org_id)
        # self.fields['doctor_department'].queryset = Department.objects.filter(department_org__exact = org_id)
        self.HOSPITAL_CHOICES = hospitalChoices(org_id)
        self.DEPT_CHOICES = departmentChoices(org_id)
        self.fields['hospital_choice'].choices = [('', 'Select a Hospital|Branch Code')] + list(hospitalChoices(org_id))
        self.fields['dept_choice'].choices = [('', 'Select a Department|Dept Code')] + list(departmentChoices(org_id))

    class Meta:
        model = DoctorRegistration
        fields = ('doctor_status',)


class PortalDoctorDetailsForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PortalDoctorDetailsForm,self).__init__(*args,**kwargs)
        self.fields['doctor_qualification'] = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = DoctorDetails
        exclude = ('doctor_id','doctor_address','doctor_date_joined','doctor_date_left',)

class PortalDoctorSelectionForm(forms.Form):
    # choices = orgs = forms.ModelChoiceField(queryset=Hospital.objects.all(),empty_label="Select Hospital")
    DOC_CHOICES = []
    choices = forms.ChoiceField(choices=DOC_CHOICES)

    def __init__(self,org_id, *args, **kwargs):
        super(PortalDoctorSelectionForm, self).__init__(*args, **kwargs)
        self.QS_CHOICES = hospitalChoices(org_id)
        self.fields['choices'].choices = [('', 'Select a Doctor|Doctor Code')] + list(doctorChoices(org_id))

class PortalOrgSettingsForm(forms.ModelForm):

    class Meta:
        model = OrgSettings
        exclude = ('orgsettings_subscription','orgsettings_subscription_rate','orgsettings_status','orgsettings_marketplace',)

class PortalHospitalSettingsForm(forms.ModelForm):

    class Meta:
        model = HospitalSettings
        fields = '__all__'

class PortalDoctorSettingsForm(forms.ModelForm):

    class Meta:
        model = DoctorSettings
        fields = '__all__'

def hospitalChoices(org_id):
    choices = []
    hospitals = Hospital.objects.filter(hospital_org__exact = org_id)
    for hospital in hospitals:
        choice = (hospital.hospital_id , hospital.hospital_name + '|' + hospital.hospital_branch_code)
        choices.append(choice)
    return choices

def departmentChoices(org_id):
    choices = []
    departments = Department.objects.filter(department_org__exact = org_id)
    for department in departments:
        choice = (department.department_id, department.department_name + '|' + department.department_code)
        choices.append(choice)
    return choices


def doctorChoices(org_id):
    choices = []
    docReg = DoctorRegistration.objects.filter(doctor_org = org_id)
    for doctor in docReg:
        details = DoctorDetails.objects.get(doctor_id = doctor.doctor_id)
        choice = (doctor.doctor_id,details.doctor_first_name+' '+details.doctor_last_name + '|' + doctor.doctor_code)
        choices.append(choice)
    return choices