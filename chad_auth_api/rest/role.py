from chad_auth_api.models import Role
from chad_auth_api.rest.helper import *
from chad_auth_api.schemas.role import RoleSchemaOut, RoleSchemaIn


class RoleResource(object):

    def __init__(self, api: NinjaAPI):
        register(
            {
                PATH: '/role', MODEL_NAME: Role, SCHEMA_OUT: RoleSchemaOut, SCHEMA_IN: RoleSchemaIn},
            api
        )
