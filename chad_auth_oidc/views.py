from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from ninja import NinjaAPI, Form

from chad_auth_api.models import Realm, Client, User
from chad_auth_api.rest import exception_handler
from chad_auth_api.rest.exception_handler import CustomAPIException, default_errors
from chad_auth_oidc.oidc_helper.auth import Util as auth_util
from chad_auth_oidc.oidc_helper.cookie import Util as cookie_util
from chad_auth_oidc.oidc_helper.jwt import Util as jwt_util
from chad_auth_oidc.schemas.oidc import OidcConfiguration, OidcToken, OidcUserInfo, RedirectUri

api = NinjaAPI(urls_namespace='oidc-api')

exception_handler.register(api)


@api.get('/{realm_name}/.well-known/openid-configuration', tags=['OIDC'], summary='returns the OIDC configurations', response={200: OidcConfiguration, **default_errors})
def well_known_open_id_conf(request: HttpRequest, realm_name: str):
    get_object_or_404(Realm, name=realm_name)
    oidc_configuration = OidcConfiguration.create(realm_name)
    return api.create_response(request, oidc_configuration, status=200)


@api.get('/{realm_name}/auth', tags=['OIDC'], summary='entry point for the authorization flow', response={302: None, **default_errors})
def authorize(request: HttpRequest, realm_name: str, client_id: str, redirect_uri: str, state: str):
    client = get_object_or_404(
        Client,
        client_id=client_id,
        realm__name=realm_name
    )

    if redirect_uri in client.redirect_uris or '*' in client.redirect_uris:
        user_id = cookie_util.extract_user_id_from_cookie(realm_name, request)
        user = None
        if user_id is not None:
            user = User.objects.filter(id=user_id).first()
        if user is not None:
            uri = RedirectUri.create(realm_name,user, redirect_uri, state)['redirect_uri']
            response = api.create_response(request, {}, status=302)
            response.headers.__setitem__('Location',uri)
            cookie_util.append_user_cookie(realm_name, user_id, response)
            return response
        else:
            return redirect(f'/login?realm={realm_name}&client_id={client_id}&redirect_uri={redirect_uri}&state={state}')
    else:
        raise CustomAPIException.bad_request(f'invalid redirect_uri: {redirect_uri}')


@api.post('/{realm_name}/auth', tags=['OIDC'], summary='username and password validation for the given realm', response={200: RedirectUri, **default_errors})
def authorize_username_password(request: HttpRequest,
                                realm_name: str,
                                username: str = Form(...),
                                password: str = Form(...),
                                client_id: str = Form(...),
                                redirect_uri: str = Form(...),
                                state: str = Form(...),
                                response_type: str = Form('code')
                                ):
    if response_type != 'code':
        raise CustomAPIException.bad_request(f'invalid response_type: {redirect_uri}, only "code" is supported')

    client = get_object_or_404(
        Client,
        client_id=client_id,
        realm__name=realm_name
    )
    if redirect_uri in client.redirect_uris or '*' in client.redirect_uris:
        hashed_password = User.hash_password(password)
        user = get_object_or_404(User, username=username, realm__name=realm_name, password=hashed_password)
        response = api.create_response(request,
                                       RedirectUri.create(realm_name, user, redirect_uri, state),
                                       status=200
                                       )
        cookie_util.append_user_cookie(realm_name, user.id, response)
        return response
    else:
        raise CustomAPIException.bad_request(f'invalid redirect_uri: {redirect_uri}')


@api.post('/{realm_name}/token', tags=['OIDC'], summary='the OIDC token endpoint', response={200: OidcToken, **default_errors})
def token(request: HttpRequest, realm_name: str,
          code: str = Form(None),
          client_id: str = Form(...),
          client_secret: str = Form(...),
          grant_type: str = Form(...)
          ):

    get_object_or_404(
        Client,
        client_id=client_id,
        client_secret=client_secret,
        realm__name=realm_name
    )

    if grant_type == 'authorization_code':
        data = jwt_util.extract_data_if_valid(code)
        if data is None:
            raise CustomAPIException.bad_request(f'the code was invalid')
        if not data['iss'].endswith(f'/oidc/{realm_name}'):
            raise CustomAPIException.bad_request(f'the code contained the wrong issuer')
        user_id = data['user_id']
        return {'access_token': jwt_util.generate_jwt_access_token(realm_name, user_id), "expires_in":300, "refresh_expires_in":0, "token_type": "Bearer", "scope": "email profile"}
    elif grant_type == 'client_credentials':
        return jwt_util.generate_jwt_token(realm_name, {'preferred_username': client_id})


@api.get('/{realm_name}/token/introspect', tags=['OIDC'], summary='the OIDC token introspect endpoint')
def introspect(request: HttpRequest, realm_name: str):
    return api.create_response(request, {'detail': 'not implemented yet'}, status=500)


@api.get('/{realm_name}/userinfo', tags=['OIDC'], summary='the OIDC userinfo endpoint', response={200: OidcUserInfo, **default_errors})
def userinfo(request: HttpRequest, realm_name: str):
    bearer_token = auth_util.extract_bearer_token(request)
    data = OidcUserInfo.create(realm_name, bearer_token)
    if data is None:
        raise CustomAPIException.bad_request(f'the token was invalid')
    if not data['iss'].endswith(f'/oidc/{realm_name}'):
        raise CustomAPIException.bad_request(f'the code contained the wrong issuer')
    return data


@api.get('/{realm_name}/logout', tags=['OIDC'], summary='the OIDC logout endpoint')
def logout(request: HttpRequest, realm_name: str):
    cookie_util.clear_cookie(realm_name, request)
    return api.create_response(request, {'detail': 'not implemented yet'}, status=500)


@api.get('/{realm_name}/certs', tags=['OIDC'], summary='the OIDC certs endpoint')
def certs(request: HttpRequest, realm_name: str):
    return api.create_response(request, {'detail': 'not implemented yet'}, status=500)
