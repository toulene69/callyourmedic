from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from django.db import IntegrityError, transaction

from utils.app_utils import getPasswordHash, checkPassword, generateAuthToken
from utils.api_response import *

from doctors.models import DoctorDetails, DoctorRegistration
from organisations.models import Apikey,Organisation, OrgSettings
from patients.models import PatientAuthToken, Patients , mail_to_send_patient
from marketplace.models import Marketplace
from serializers import *

import traceback
import logging

logger = logging.getLogger('webapi')
request_logr = logging.getLogger('django.request')
HTTP_METHOD = ' HTTP Method | '
API_KEY = ' API_KEY | '
MSG = ' Messge | '

# class DoctorList(generics.ListCreateAPIView):
#
#     queryset = DoctorDetails.objects.filter(doctor_id__in = DoctorRegistration.objects.filter(doctor_org = 6))
#     serializer_class = DoctorDetailSerializer
#

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    try:
        usertype = request.data['usertype']
        if usertype == 'patient':
            return patient_login(request)
        elif usertype == 'doctor' :
            return doctor_login(request)
        else:

            raise Exception()
    except:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def logout(request):
    try:
        usertype = request.GET['usertype']
        if usertype == 'patient':
            return patient_logout(request)
        elif usertype == 'doctor' :
            return doctor_logout(request)
        else:
            print "except"
            raise Exception()
    except:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def passwordchange(request):
    if 'apikey' not in request.data:

        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)
    try:
        usertype = request.data['usertype']
        if usertype == 'patient':
            print("hello")
            return patient_change_password(request)
        elif usertype == 'doctor' :
            return doctor_change_password(request)
        else:
            print "except"
            raise Exception()
    except:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)


""" Patient Login/Logout/Create/Update apis """


def patient_login(request):
    ## check for request data
    try:
        apikey = request.data['apikey']
        emailid = request.data['emailid']
        password = request.data['password']
    except:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)
    LOG_STR = HTTP_METHOD + request.method +',' + API_KEY + apikey + ',' + MSG
    key = None
    patient = None
    ## check for apikey

    isMarketplace = False
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info(LOG_STR +"Not a marketplace app request")
    if isMarketplace is False:
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)
        except(KeyError, Apikey.DoesNotExist):
            return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)
        ## check for apikey status
        if key.apikey_status :
            ## check for patient
            try:
                patient = Patients.objects.get(patient_org = key.apikey_org, patient_email = emailid)
            except(KeyError,Patients.DoesNotExist):
                return Response(HTTP_RESPONSE_MSG_FOR_USER_NOT_EXISTS,status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)

    else:
        try:
            patient = Patients.objects.get(patient_email = emailid, patient_ismarketplace = True)
        except(KeyError,Patients.DoesNotExist):
            return Response(HTTP_RESPONSE_MSG_FOR_USER_NOT_EXISTS,status=status.HTTP_404_NOT_FOUND)
    ## password check

    if checkPassword(password,patient.patient_password):
        tok = generateAuthToken()
        patientAuthTokObj = None
        patient_tokens_array = PatientAuthToken.objects.filter(patient_id = patient.patient_id)
        if len(patient_tokens_array) == 0 :
            patientAuthTokObj = PatientAuthToken()
            patientAuthTokObj.patient = patient
        elif len(patient_tokens_array) == 1 :
            patientAuthTokObj = patient_tokens_array[0]
        else:
            Response(HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        patientAuthTokObj.patient_token = tok
        try:
            patientAuthTokObj.save()
        except:
            Response(HTTP_RESPONSE_MSG_FOR_USER_LOGIN_ERROR,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        result = {}
        result['auth_token'] = patientAuthTokObj.patient_token
        return Response(result,status=status.HTTP_200_OK)
    else:
        return Response(HTTP_RESPONSE_MSG_FOR_USER_WRONG_PASSWORD,status=status.HTTP_400_BAD_REQUEST)

def patient_logout(request):

    try:
        apikey = request.GET['apikey']
        authtoken = request.GET['authtoken']
    except:

        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)
    LOG_STR = HTTP_METHOD + request.method +',' + API_KEY + apikey + ',' + MSG

    isMarketplace = False
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info(LOG_STR +"Not a marketplace app request")

    if isMarketplace is False:
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)

        except(KeyError, Apikey.DoesNotExist):
            return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)
        if key.apikey_status is False:
            return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)

    patientAuthTokObj = None
    patient_tok_array = PatientAuthToken.objects.filter(patient_token__exact = authtoken)

    if len(patient_tok_array) == 1:
        patientAuthTokObj = patient_tok_array[0]
    else:
        return Response(HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID,status=status.HTTP_401_UNAUTHORIZED)
    if isMarketplace:
        patientAuthTokObj.patient_token = ''
        patientAuthTokObj.save()
        return Response(HTTP_RESPONSE_MSG_FOR_USER_LOGOUT_SUCCESS,status=status.HTTP_200_OK)
    else:
        if patientAuthTokObj.patient.patient_org.org_id == key.apikey_org.org_id :
            patientAuthTokObj.patient_token = ''
            patientAuthTokObj.save()
            return Response(HTTP_RESPONSE_MSG_FOR_USER_LOGOUT_SUCCESS,status=status.HTTP_200_OK)
        else:
            return Response(HTTP_RESPONSE_MSG_FOR_USER_AUTH_APIKEY_ERROR,status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET','POST','PUT'])         ######## For Creating and updating patients  #########
@permission_classes((permissions.AllowAny,))
def patient(request):
    if 'apikey' not in request.data:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        return create_patient(request)

    if request.method == 'PUT':
        return update_patient(request)

    if request.method == 'GET':
        patients = Patients.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


def create_patient(request):

    apikey = request.data['apikey']
    LOG_STR = HTTP_METHOD + request.method +',' + API_KEY + apikey + ',' + MSG
    if 'emailid' not in request.data or 'password' not in request.data or 'phone' not in request.data:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)

    emailid = request.data['emailid']
    password = request.data['password']
    phone = request.data['phone']
    isMarketplace = False
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info(LOG_STR +"Not a marketplace app request")

    if isMarketplace:
        try:
            patient_exsits = Patients.objects.get(patient_email = emailid)
            if patient_exsits is not None :
                logger.error(LOG_STR +"Patient Creation : Already exists for marketplace app with emailid ["+emailid+"]")
                return Response(HTTP_RESPONSE_MSG_FOR_USER_ALREADY_EXISTS,status=status.HTTP_409_CONFLICT)
        except(KeyError, Patients.DoesNotExist):
            logger.info(LOG_STR +"Patient Creation for marketplace : New Email id ["+emailid+"]")
    else:
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)
            if key.apikey_status :
                try:
                    patient_exsits = Patients.objects.get(patient_org = key.apikey_org, patient_email = emailid)
                    if patient_exsits is not None :
                        logger.error(LOG_STR +"Patient Creation : Already exists with emailid ["+emailid+"]")
                        return Response(HTTP_RESPONSE_MSG_FOR_USER_ALREADY_EXISTS,status=status.HTTP_409_CONFLICT)
                except(KeyError, Patients.DoesNotExist):
                    logger.info(LOG_STR +"Patient Creation : New Email id ["+emailid+"]")
                # patient = Patients(patient_org = key.apikey_org, patient_email = emailid, patient_password = password, patient_phone1 = phone)
            else:
                return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)
        except(KeyError, Apikey.DoesNotExist):
            return  Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)

    dict = {}
    dict['patient_email'] = emailid
    dict['patient_phone1'] = phone
    dict['patient_password'] = getPasswordHash(password)
    if isMarketplace:
        dict['patient_org'] = None
    else:
        dict['patient_org'] = key.apikey_org.org_id
    patientserializer = PatientSerializer(data = dict)
    if patientserializer.is_valid():
        try:
            patient = None
            with transaction.atomic():
                if isMarketplace:
                    patient = Patients(patient_org = None, patient_email = dict['patient_email'], patient_password = dict['patient_password'],
                patient_phone1 = dict['patient_phone1'], patient_ismarketplace = True)
                else:
                    patient = Patients(patient_org = key.apikey_org, patient_email = dict['patient_email'], patient_password = dict['patient_password'],
                patient_phone1 = dict['patient_phone1'])
                patient.save()
                patient_tok = PatientAuthToken()
                patient_tok.patient = patient
                patient_tok.patient_token = ''
                patient_tok.save()
            mail_to_send_patient(patient)
            return Response(HTTP_RESPONSE_MSG_FOR_USER_CREATED,status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(HTTP_RESPONSE_MSG_FOR_USER_CREATE_DB_ERROR,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(patientserializer.errors,status=status.HTTP_400_BAD_REQUEST)

def update_patient(request):
    apikey = request.data['apikey']
    LOG_STR = HTTP_METHOD + request.method +',' + API_KEY + apikey + ',' + MSG
    """check apikey"""
    key = None

    isMarketplace = False
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info(LOG_STR +"Not a marketplace app request")

    if isMarketplace is False:
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)
            if key.apikey_status == False :
                return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)
        except(KeyError, Apikey.DoesNotExist):
            return  Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)
    authtoken = None
    """Check auth token"""
    try:
        authtoken = request.data['authtoken']
    except:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)

    patient_token_array = PatientAuthToken.objects.filter(patient_token__exact = authtoken)
    patientAuthObj = None
    if len(patient_token_array) == 0:
        return Response(HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID,status=status.HTTP_401_UNAUTHORIZED)
    elif len(patient_token_array) > 1:
        return Response(HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        patientAuthObj = patient_token_array[0]

    if isMarketplace is False:
        if patientAuthObj.patient.patient_org.org_id != key.apikey_org.org_id :
            return Response(HTTP_RESPONSE_MSG_FOR_USER_AUTH_APIKEY_ERROR,status=status.HTTP_401_UNAUTHORIZED)
    patient_dict = {}
    address_dict = {}

    if 'phone' in request.data:
        patient_dict['patient_phone1'] = request.data['phone']
    if 'first_name' in request.data:
        patient_dict['patient_first_name'] = request.data['first_name']
    if 'last_name' in request.data:
        patient_dict['patient_last_name'] = request.data['last_name']
    if 'dob' in request.data:
        patient_dict['patient_dob'] = request.data['dob']
    if 'gender' in request.data:
        patient_dict['patient_gender'] = request.data['gender'].upper()
    if 'address_line1' in request.data:
        address_dict['address_line1'] = request.data['address_line1']
    if 'address_line2' in request.data:
        address_dict['address_line2'] = request.data['address_line2']
    if 'city' in request.data:
        address_dict['address_city'] = request.data['city']
    if 'state' in request.data:
        address_dict['address_state'] = request.data['state'].upper()
    if 'zipcode' in request.data:
        address_dict['address_pincode'] = request.data['zipcode']

    patientserializer = PatientSerializer(data = patient_dict,partial=True)
    addressserializer = AddressSerializer(data = address_dict,partial=True)
    if patientserializer.is_valid() is False:
        return Response(patientserializer.errors,status=status.HTTP_400_BAD_REQUEST)
    if addressserializer.is_valid() is False:
        return Response(addressserializer.errors,status=status.HTTP_400_BAD_REQUEST)

    patient = patientAuthObj.patient
    if 'patient_first_name' in patientserializer.validated_data:
        patient.patient_first_name = patientserializer.validated_data['patient_first_name']
    if 'patient_last_name' in patientserializer.validated_data:
        patient.patient_last_name = patientserializer.validated_data['patient_last_name']
    if 'patient_gender' in patientserializer.validated_data:
        patient.patient_gender = patientserializer.validated_data['patient_gender']
    if 'patient_dob' in patientserializer.validated_data:
        patient.patient_dob = patientserializer.validated_data['patient_dob']
    if 'patient_phone1' in patientserializer.validated_data:
        patient.patient_phone1 = patientserializer.validated_data['patient_phone1']

    address = None
    if patientAuthObj.patient.patient_address is None :
        address = Address()
    else:
        address = patientAuthObj.patient.patient_address

    if 'address_line1' in addressserializer.validated_data:
        address.address_line1 = addressserializer.validated_data['address_line1']
    else:
        address.address_line1 = ''
    if 'address_line2' in addressserializer.validated_data :
        address.address_line2 = addressserializer.validated_data['address_line2']
    else:
        address.address_line2 = ''
    if 'address_city' in addressserializer.validated_data :
        address.address_city = addressserializer.validated_data['address_city']
    else:
        address.address_city = ''
    if 'address_state' in addressserializer.validated_data :
        address.address_state = addressserializer.validated_data['address_state']
        print(address.address_state)
    else:
        address.address_state = ''
    if 'address_pincode' in addressserializer.validated_data :
        address.address_pincode = addressserializer.validated_data['address_pincode']
    else:
        address.address_pincode = 0
    try:
        with transaction.atomic():
            print(address)
            address.save()
            patient.patient_address = address
            patient.save()
        result = PatientSerializer(patient)
        return Response(result.data,status=status.HTTP_200_OK)
    except :
        traceback.print_exc()
        return Response(HTTP_RESPONSE_MSG_FOR_USER_UPDATE_ERROR,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def patient_change_password(request):
    apikey = None
    authtoken = None
    currentpassword = None
    newpassword = None
    try:
        apikey = request.data['apikey']
        authtoken = request.data['authtoken']
        currentpassword = request.data['currentpassword']
        newpassword = request.data['newpassword']
    except:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)
    key = None

    isMarketplace = False
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info("Not a marketplace app request")

    if isMarketplace is False:
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)
            if key.apikey_status == False :
                return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)
        except(KeyError, Apikey.DoesNotExist):
            return  Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)

    patient_token_array = PatientAuthToken.objects.filter(patient_token__exact = authtoken)
    patientAuthObj = None
    if len(patient_token_array) == 0:
        return Response(HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID,status=status.HTTP_401_UNAUTHORIZED)
    elif len(patient_token_array) > 1:
        return Response(HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        patientAuthObj = patient_token_array[0]

    if isMarketplace is False:
        if patientAuthObj.patient.patient_org.org_id != key.apikey_org.org_id :
            return Response(HTTP_RESPONSE_MSG_FOR_USER_AUTH_APIKEY_ERROR,status=status.HTTP_401_UNAUTHORIZED)

    if newpassword is None or len(newpassword)==0:
        return Response(HTTP_RESPONSE_MSG_FOR_PASSWORD_UPDATE_ERROR_EMPTY,status=status.HTTP_400_BAD_REQUEST)

    patient = patientAuthObj.patient
    if checkPassword(currentpassword,patient.patient_password):
        newpass = getPasswordHash(newpassword)
        newtok = generateAuthToken()
        patient.patient_password = newpass
        patientAuthObj.patient_token = newtok
        try:
            with transaction.atomic():
                patient.save()
                patientAuthObj.save()
            result = PatientAuthTokenSerializer(patientAuthObj)
            return Response(result.data,status=status.HTTP_200_OK)
        except:
            return Response(HTTP_RESPONSE_MSG_FOR_USER_UPDATE_ERROR,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(HTTP_RESPONSE_MSG_FOR_PASSWORD_UPDATE_ERROR_CURRENT_PASSWORD_MISMATCH,status=status.HTTP_400_BAD_REQUEST)
""""""""""" Patient Ends  """""""""""

"""""Orgs for Marketplace app """""
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def orgs(request):
    apikey = None
    if 'apikey' not in request.GET :
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)
    if 'authtoken' not in request.GET:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)
    apikey = request.GET['apikey']
    authtoken = request.GET['authtoken']

    isMarketplace = False
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info("Not a marketplace app request to fetch org list")
        return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)

    patient_token_array = PatientAuthToken.objects.filter(patient_token__exact = authtoken)
    patientAuthObj = None
    if len(patient_token_array) == 0:
        return Response(HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID,status=status.HTTP_401_UNAUTHORIZED)
    elif len(patient_token_array) > 1:
        return Response(HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        patientAuthObj = patient_token_array[0]

    mp_organisations = Organisation.objects.filter(org_active = 'A', org_settings__in = OrgSettings.objects.filter(orgsettings_marketplace = True).values('orgsettings_id'))\
        .values('org_name','org_brand','org_identifier')

    orgserializer = OrgSerializer(mp_organisations,many = True)
    return Response(orgserializer.data,status=status.HTTP_200_OK)


"""""Orgs Ends """""

""""""" Department """""""
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def departments(request):
    apikey = None
    if 'apikey' not in request.GET :
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)
    if 'authtoken' not in request.GET:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)
    isMarketplace = False

    apikey = request.GET['apikey']
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info("Not a marketplace app request to fetch org list")

    org = None
    if isMarketplace:
        if 'orgid' not in request.GET:
            return Response(HTTP_RESPONSE_MSG_FOR_NO_ORG_IDENTIFIER_FOR_DEPT,status=status.HTTP_400_BAD_REQUEST)
        else:
            orgidentifier = request.GET['orgid']
            orgList = Organisation.objects.filter(org_identifier__iexact = orgidentifier)
            if len(orgList) == 0:
                return Response(HTTP_RESPONSE_MSG_FOR_NO_ORG_IDENTIFIER_FOR_DEPT,status=status.HTTP_400_BAD_REQUEST)
            elif len(orgList) > 1:
                return Response(HTTP_RESPONSE_MSG_FOR_ORG_DB_ERROR,status=status.HTTP_400_BAD_REQUEST)
            else:
                org = orgList[0]
    else:
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)
            if key.apikey_status == False :
                return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)
        except(KeyError, Apikey.DoesNotExist):
            return  Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)

    authtoken = request.GET['authtoken']
    """Check auth token"""
    patient_token_array = PatientAuthToken.objects.filter(patient_token__exact = authtoken)
    patientAuthObj = None
    if len(patient_token_array) == 0:
        return Response(HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID,status=status.HTTP_401_UNAUTHORIZED)
    elif len(patient_token_array) > 1:
        return Response(HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        patientAuthObj = patient_token_array[0]

    if isMarketplace is False:
        if patientAuthObj.patient.patient_org.org_id != key.apikey_org.org_id :
            return Response(HTTP_RESPONSE_MSG_FOR_USER_AUTH_APIKEY_ERROR,status=status.HTTP_401_UNAUTHORIZED)

    departments = None
    if isMarketplace:
        departments = Department.objects.filter(department_org__exact = org, department_status=True)
    else:
        departments = Department.objects.filter(department_org__exact = key.apikey_org, department_status=True)
    departmentserializer = DepartmentSerializer(departments,many=True)
    return Response(departmentserializer.data,status=status.HTTP_200_OK)


class DepartmentList(generics.ListCreateAPIView):
    org = None
    status = True
    queryset = Department.objects.filter(department_org__exact = 6, department_status=True)
    serializer_class = DepartmentSerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        apikey = None
        if 'apikey' not in request.GET :
            return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)
        if 'authtoken' not in request.GET:
            return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)

        apikey = request.GET['apikey']
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)
            if key.apikey_status == False :
                return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)
        except(KeyError, Apikey.DoesNotExist):
            return  Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)
        authtoken = request.GET['authtoken']
        """Check auth token"""
        patient_token_array = PatientAuthToken.objects.filter(patient_token__exact = authtoken)
        patientAuthObj = None
        if len(patient_token_array) == 0:
            return Response(HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID,status=status.HTTP_401_UNAUTHORIZED)
        elif len(patient_token_array) > 1:
            return Response(HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            patientAuthObj = patient_token_array[0]

        if patientAuthObj.patient.patient_org.org_id != key.apikey_org.org_id :
            return Response(HTTP_RESPONSE_MSG_FOR_USER_AUTH_APIKEY_ERROR,status=status.HTTP_401_UNAUTHORIZED)
        # self.org = 6
        # self.status = True
        queryset = Department.objects.filter(department_org__exact = key.apikey_org, department_status=True)
        print queryset
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)


""""""" Department Ends"""""""

""""""" Doctors """""""
def doctor_login(request):
    res = {}
    res['message'] = 'Work in progress!!!'
    return Response(ResponseMessageSerializer(res).data,status=status.HTTP_404_NOT_FOUND)

def doctor_logout(request):
    return Response(status=status.HTTP_404_NOT_FOUND)

def doctor_change_password(request):
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def doctors(request):
    apikey = None
    if 'apikey' not in request.GET :
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)
    if 'authtoken' not in request.GET:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_401_UNAUTHORIZED)
    if 'department_code' not in request.GET:
        return Response(HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED,status=status.HTTP_400_BAD_REQUEST)
    apikey = request.GET['apikey']
    isMarketplace = False
    try:
        mp_key = Marketplace.objects.get(apikey__exact = apikey)
        isMarketplace = True
    except:
        logger.info("Not a marketplace app request to fetch org list")

    org = None
    if isMarketplace:
        if 'orgid' not in request.GET:
            return Response(HTTP_RESPONSE_MSG_FOR_NO_ORG_IDENTIFIER_FOR_DEPT,status=status.HTTP_400_BAD_REQUEST)
        else:
            orgidentifier = request.GET['orgid']
            orgList = Organisation.objects.filter(org_identifier__iexact = orgidentifier)
            if len(orgList) == 0:
                return Response(HTTP_RESPONSE_MSG_FOR_NO_ORG_IDENTIFIER_FOR_DEPT,status=status.HTTP_400_BAD_REQUEST)
            elif len(orgList) > 1:
                return Response(HTTP_RESPONSE_MSG_FOR_ORG_DB_ERROR,status=status.HTTP_400_BAD_REQUEST)
            else:
                org = orgList[0]
    else:
        try:
            key = Apikey.objects.get(apikey_key__exact = apikey)
            if key.apikey_status == False :
                return Response(HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED,status=status.HTTP_401_UNAUTHORIZED)
        except(KeyError, Apikey.DoesNotExist):
            return  Response(HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID,status=status.HTTP_401_UNAUTHORIZED)

    authtoken = request.GET['authtoken']
    """Check auth token"""
    patient_token_array = PatientAuthToken.objects.filter(patient_token__exact = authtoken)
    patientAuthObj = None
    if len(patient_token_array) == 0:
        return Response(HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID,status=status.HTTP_401_UNAUTHORIZED)
    elif len(patient_token_array) > 1:
        return Response(HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        patientAuthObj = patient_token_array[0]
    if isMarketplace is False:
        if patientAuthObj.patient.patient_org.org_id != key.apikey_org.org_id :
            return Response(HTTP_RESPONSE_MSG_FOR_USER_AUTH_APIKEY_ERROR,status=status.HTTP_401_UNAUTHORIZED)

    department = None
    departments_array = None
    department_code = request.GET['department_code']
    if isMarketplace:
        departments_array = Department.objects.filter(department_org__exact = org,department_code__exact = department_code)
    else:
        departments_array = Department.objects.filter(department_org__exact = key.apikey_org,department_code__exact = department_code)
    if len(departments_array) == 0:
        return Response(HTTP_RESPONSE_MSG_FOR_NO_DEPARTMENT_FOUND,status=status.HTTP_404_NOT_FOUND)
    elif len(departments_array) > 1 :
        return Response(HTTP_RESPONSE_MSG_FOR_MULTIPLE_DEPARTMENT_FOUND,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        department = departments_array[0]

    queryset = None
    if isMarketplace:
        queryset = DoctorDetails.objects.filter(doctor_id__in = DoctorRegistration.objects.filter(doctor_org = org,doctor_department = department))
    else:
        queryset = DoctorDetails.objects.filter(doctor_id__in = DoctorRegistration.objects.filter(doctor_org = key.apikey_org,doctor_department = department))
    departmentserializer = DoctorDetailSerializer(queryset,many=True)
    return Response(departmentserializer.data,status=status.HTTP_200_OK)


""""""" Doctors """""""