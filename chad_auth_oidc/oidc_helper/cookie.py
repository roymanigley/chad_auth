import datetime
import uuid

from django.http import HttpRequest, HttpResponse

from chad_auth.settings import OIDC_SESSION_LIFE_TIME_SECONDS
from chad_auth_oidc.oidc_helper.jwt import Util as jwt_util

_COOKIE_KEY = 'CHAD_AUTH_USER_SESSION'
_USER_ID_KEY = 'CHAD_AUTH_USER_ID'


class __Util(object):

    @staticmethod
    def append_user_cookie(realm_name: str, user_id: uuid.UUID, response: HttpResponse) -> None:
        token = jwt_util.generate_jwt_token(realm_name, {_USER_ID_KEY: str(user_id)}, OIDC_SESSION_LIFE_TIME_SECONDS)
        expires = datetime.datetime.now() + datetime.timedelta(seconds=OIDC_SESSION_LIFE_TIME_SECONDS)
        response.set_cookie(f'{_COOKIE_KEY}-{realm_name}', token, expires=expires)

    @staticmethod
    def extract_user_id_from_cookie(realm_name: str, request: HttpRequest) -> str or None:
        cookie = request.COOKIES.get(f'{_COOKIE_KEY}-{realm_name}')
        if cookie is not None:
            decoded_cookie = jwt_util.extract_data_if_valid(cookie)
            if decoded_cookie is not None and decoded_cookie['iss'].endswith(f'/oidc/{realm_name}'):
                return decoded_cookie[_USER_ID_KEY]
        return None

    @staticmethod
    def clear_cookie(realm_name: str, request: HttpRequest) -> None:
        cookie_key = f'{_COOKIE_KEY}-{realm_name}'
        if request.COOKIES.get(cookie_key):
            request.COOKIES.pop(cookie_key)


Util = __Util()
