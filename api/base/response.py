from rest_framework import status
from rest_framework.exceptions import APIException

class CustomAPIException(APIException):
    def __init__(self, error, mess , status_code):
        self.status_code = status_code
        self.detail = {
            'status_code': status_code,
            'error':error,
            'data':None,
            'mess': mess,
        }