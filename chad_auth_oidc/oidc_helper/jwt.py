from datetime import datetime

import jwt
from django.shortcuts import get_object_or_404

from chad_auth.settings import OIDC_ACCESS_TOKEN_LIFE_TIME_SECONDS
from chad_auth_api.models import User, UserRole
from chad_auth_oidc.oidc_helper.keys import Util as key_util


class __Util(object):

    @staticmethod
    def generate_jwt_access_token(realm_name, user_id) -> str:
        user = get_object_or_404(User, id=user_id)
        user_roles = UserRole.objects.filter(user_id=user.id).values()
        scopes = ['openid']
        token = Util.generate_jwt_token(realm_name, {
            "aud": "account",
            "resource_access": {
                "account": {
                    "roles": [user_role.role.name for user_role in user_roles]
                }
            },
            "scope": ' '.join(scopes),
            "preferred_username": user.username,
        }, OIDC_ACCESS_TOKEN_LIFE_TIME_SECONDS)
        return token

    @staticmethod
    def generate_jwt_token(realm_name: str, data: dict, seconds_to_live=60) -> str:
        timestamp_now = int(datetime.now().timestamp())
        timestamp_expiration = timestamp_now + seconds_to_live
        token_body = {
            "exp": timestamp_expiration,
            "iat": timestamp_now,
            "iss": f"http://localhost:8080/oidc/{realm_name}",
            "aud": "account"
        }
        token_body.update(data)
        return jwt.encode(token_body, key_util.load_private_key(), algorithm='HS256')

    @staticmethod
    def extract_data_if_valid(token: str) -> dict or None:
        try:
            return jwt.decode(token, key_util.load_private_key(), algorithms='HS256', audience='account')
        except Exception as e:
            print(e)
            return None


Util = __Util()
