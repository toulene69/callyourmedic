__author__ = 'apoorv'


from rest_framework import serializers
from hospitals.models import Department, Hospital
from doctors.models import DoctorRegistration, DoctorDetails
from patients.models import Patients, PatientAuthToken
from addresses.models import Address
from organisations.models import Organisation


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        field = ('address_line1','address_line2','address_city','address_state','address_pincode')
        exclude = ('address_id','address_status')

class OrgSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='org_name')
    brand = serializers.CharField(source='org_name')

    class Meta:
        model = Organisation
        field = ('org_identifier')
        exclude = ('org_id','org_emailid','org_phone','org_active','org_address','org_date_joined','org_date_left','org_billing_id','org_settings','org_brand','org_name')

class HospitalSerializer(serializers.ModelSerializer):

    hospital_address = AddressSerializer()

    class Meta:
        model = Hospital
        field = ('hospital_name','hospital_address')
        exclude = ('hospital_id','hospital_org','hospital_branch_code','hospital_email_id','hospital_phone1','hospital_phone2','hospital_status','hospital_date_joined',
                   'hospital_date_left', 'hospital_settings',)

class DepartmentSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=200,source='department_name')
    description = serializers.CharField(max_length=200,allow_null=True,source='department_description')
    code = serializers.CharField(max_length=10,source='department_code')


class DoctorRegistrationSerializer(serializers.ModelSerializer):

    hospital = HospitalSerializer(source='doctor_hospital')
    department = DepartmentSerializer(source='doctor_department')

    class Meta:
        model = DoctorRegistration
        field = ('doctor_code',)
        exclude = ('doctor_id','doctor_department','doctor_org','doctor_email','doctor_password','doctor_status','doctor_hospital','doctor_settings',)


class DoctorDetailSerializer(serializers.ModelSerializer):

    doctor_details = DoctorRegistrationSerializer(source='doctor_id')
    first_name = serializers.CharField(source='doctor_first_name')
    last_name = serializers.CharField(source='doctor_last_name')
    gender = serializers.CharField(source='doctor_gender')
    qualification = serializers.CharField(source='doctor_qualification')
    experience = serializers.IntegerField(source='doctor_experience')
    class Meta:
        model = DoctorDetails
        # field = ( 'doctor_first_name','doctor_last_name','doctor_gender', 'doctor_qualification', 'doctor_experience',)
        exclude = ('doctor_id','info_id','doctor_phone1','doctor_phone2','doctor_date_joined','doctor_date_left','doctor_address',
                   'doctor_first_name','doctor_last_name','doctor_gender', 'doctor_qualification', 'doctor_experience',)

class PatientSerializer(serializers.ModelSerializer):

    patient_address = AddressSerializer(required=False)

    class Meta:
        model = Patients
        field = ('patient_first_name','patient_last_name','patient_dob','patient_gender','patient_email','patient_phone1','patient_address')
        exclude = ('patient_password','patient_id','patient_org','patient_date_joined','patient_date_left','patient_ismarketplace')

    def validate_patient_phone1(self,value):

        if len(value) != 0 and value.isdigit() :
            return value
        else:
            raise serializers.ValidationError("Phone number field must only have digits.")


class PatientAuthTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientAuthToken
        field = ('patient_token',)
        exclude = ('id','patient')


class ResponseMessageSerializer(serializers.Serializer):

    message = serializers.CharField(max_length=200)