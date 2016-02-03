__author__ = 'apoorv'

from webapi.serializers import ResponseMessageSerializer

HTTP_RESPONSE_MSG_FOR_REQUEST_MALFORMED = ResponseMessageSerializer({'message': 'Request parameters types malformed/incorrect.'}).data

HTTP_RESPONSE_MSG_FOR_APIKEY_EXPIRED = ResponseMessageSerializer({'message': 'APIKey expired. Please contact admin.'}).data
HTTP_RESPONSE_MSG_FOR_APIKEY_INVALID = ResponseMessageSerializer({'message': 'APIKey invalid'}).data
HTTP_RESPONSE_MSG_FOR_AUTH_TOKEN_INVALID = ResponseMessageSerializer({'message':'Invalid auth token.'}).data
HTTP_RESPONSE_MSG_FOR_USER_AUTH_APIKEY_ERROR = ResponseMessageSerializer({'message': 'Please check apikey and auth token'}).data


HTTP_RESPONSE_MSG_FOR_USER_ALREADY_EXISTS = ResponseMessageSerializer({'message': 'User already exists.'}).data
HTTP_RESPONSE_MSG_FOR_USER_NOT_EXISTS = ResponseMessageSerializer({'message': 'User does not exists.'}).data
HTTP_RESPONSE_MSG_FOR_USER_CREATE_DB_ERROR = ResponseMessageSerializer({'message': 'DB Problem occured while creating User.'}).data
HTTP_RESPONSE_MSG_FOR_USER_MULTIPLE = ResponseMessageSerializer({'message': 'Multiple Users found. Please contact admin.'}).data
HTTP_RESPONSE_MSG_FOR_USER_CREATED = ResponseMessageSerializer({'message': 'User created successfully.'}).data
HTTP_RESPONSE_MSG_FOR_USER_LOGIN_ERROR = ResponseMessageSerializer({'message': 'User login error.'}).data
HTTP_RESPONSE_MSG_FOR_USER_WRONG_PASSWORD = ResponseMessageSerializer({'message': 'Incorrect username/password'}).data
HTTP_RESPONSE_MSG_FOR_USER_LOGOUT_SUCCESS = ResponseMessageSerializer({'message': 'User logout success.'}).data
HTTP_RESPONSE_MSG_FOR_USER_LOGOUT_ERROR = ResponseMessageSerializer({'message': 'User logout error'}).data
HTTP_RESPONSE_MSG_FOR_USER_UPDATE_ERROR = ResponseMessageSerializer({'message': 'Error occured while updating.'}).data
HTTP_RESPONSE_MSG_FOR_PASSWORD_UPDATE_ERROR_EMPTY = ResponseMessageSerializer({'message': 'New password is not valid.'}).data
HTTP_RESPONSE_MSG_FOR_PASSWORD_UPDATE_ERROR_CURRENT_PASSWORD_MISMATCH = ResponseMessageSerializer({'message': 'Current password does not match'}).data

HTTP_RESPONSE_MSG_FOR_NO_DEPARTMENT_FOUND = ResponseMessageSerializer({'message':'Department code not found'}).data
HTTP_RESPONSE_MSG_FOR_MULTIPLE_DEPARTMENT_FOUND = ResponseMessageSerializer({'message':'Multiple Departments found. Please contact admin.'}).data




