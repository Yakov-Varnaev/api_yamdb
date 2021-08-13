from rest_framework import status
from rest_framework.exceptions import APIException


class UsernameWasNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'There is no such user.'