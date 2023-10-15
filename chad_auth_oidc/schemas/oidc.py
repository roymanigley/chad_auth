from typing import List

from django.shortcuts import get_object_or_404
from ninja import schema

from chad_auth_api.models import User
from chad_auth_oidc.oidc_helper.jwt import Util as jwt_util
from chad_auth_oidc.oidc_helper.oidc import get_well_known_oidc_configuration


class OidcConfiguration(schema.Schema):
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    introspection_endpoint: str
    userinfo_endpoint: str
    end_session_endpoint: str
    frontchannel_logout_session_supported: str
    frontchannel_logout_supported: str
    jwks_uri: str

    @staticmethod
    def create(realm_name: str):
        return get_well_known_oidc_configuration(realm_name)


class OidcToken(schema.Schema):
    access_token: str
    expires_in: str
    refresh_expires_in: str
    token_type: str
    scope: str


class OidcAccount(schema.Schema):
    roles: List[str]


class OidcResourceAccess(schema.Schema):
    account: OidcAccount


class OidcUserInfo(schema.Schema):
    exp: str
    iat: str
    iss: str
    aud: str
    aud: str
    resource_access: OidcResourceAccess
    scope: str
    preferred_username: str
    sub: str

    @staticmethod
    def create(realm_name: str, bearer_token: str):
        data = jwt_util.extract_data_if_valid(bearer_token)
        user = get_object_or_404(User, username=data['preferred_username'], realm__name=realm_name)
        data['sub'] = str(user.id)
        return data


class RedirectUri(schema.Schema):
    redirect_uri: str

    @staticmethod
    def create(realm_name: str, user: User, redirect_uri: str, state: str):
        access_code = jwt_util.generate_jwt_access_token(realm_name, user.id)
        code = jwt_util.generate_jwt_token(realm_name, {'user_id': str(user.id)})
        return {
            'redirect_uri': f'{redirect_uri}?code={code}&access_code={access_code}&state={state}'
        }
