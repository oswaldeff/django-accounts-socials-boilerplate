from rest_framework import exceptions, status
from rest_framework.exceptions import APIException


class CustomKeyNotFoundAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'KEY NOT FOUND, PLEASE CHECK API KEY'
    default_code = 'KEY ERROR'