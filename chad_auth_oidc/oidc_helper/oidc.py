from chad_auth.settings import OIDC_BASE_URL


def get_well_known_oidc_configuration(realm_name: str) -> dict:
    return {
        'issuer': f'{OIDC_BASE_URL}/oidc/{realm_name}',
        'authorization_endpoint': f'{OIDC_BASE_URL}/oidc/{realm_name}/auth',
        'token_endpoint': f'{OIDC_BASE_URL}/oidc/{realm_name}/token',
        'introspection_endpoint': f'{OIDC_BASE_URL}/oidc/{realm_name}/token/introspect',
        'userinfo_endpoint': f'{OIDC_BASE_URL}/oidc/{realm_name}/userinfo',
        'end_session_endpoint': f'{OIDC_BASE_URL}/oidc/{realm_name}/logout',
        'frontchannel_logout_session_supported': False, # not implemented yet
        'frontchannel_logout_supported': False, # not implemented yet
        'jwks_uri': f'{OIDC_BASE_URL}/oidc/{realm_name}/certs',
    }
