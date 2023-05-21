from rest_framework.exceptions import APIException


class UnauthorizedUser(APIException):
    status_code = 401
    default_detail = {
        'detail': 'Учетные данные не были предоставлены.'}
