import base64

from django.http import HttpRequest


class __Util(object):

    @staticmethod
    def extract_basic_auth_header(request: HttpRequest) -> (str, str):
        auth_header = request.headers.get('Authorization')
        client_id = None
        client_secret = None
        if auth_header.find('Basic') == 0:
            auth_header = auth_header.replace('Basic ', '')
            decoded = base64.decodebytes(auth_header.encode('utf-8')).decode('utf-8').split(':')
            client_id = decoded[0]
            client_secret = decoded[1]
        return client_id, client_secret

    @staticmethod
    def extract_bearer_token(request: HttpRequest) -> str:
        auth_header = request.headers.get('Authorization')
        bearer_token = None
        if auth_header.find('Bearer') == 0:
            bearer_token = auth_header.replace('Bearer ', '')
        return bearer_token


Util = __Util()
