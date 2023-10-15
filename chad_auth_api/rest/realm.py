from chad_auth_api.models import Realm
from chad_auth_api.rest.exception_handler import CustomAPIException
from chad_auth_api.rest.helper import *
from chad_auth_api.schemas.realm import RealmSchemaOut, RealmSchemaIn


class RealmResource(object):

    def __init__(self, api: NinjaAPI):
        register(
            {
                PATH: '/realm', MODEL_NAME: Realm, SCHEMA_OUT: RealmSchemaOut, SCHEMA_IN: RealmSchemaIn,
                ALLOW_CREATE: False, ALLOW_UPDATE: False
             },
            api
        )

        @api.post('/realm', response={201: RealmSchemaOut, **default_errors},
                  tags=['Realm'], summary='creates a new record')
        def post(request: HttpRequest, payload: RealmSchemaIn):
            if payload.name.find('/') > -1 or payload.name.find(' ') > -1:
                raise CustomAPIException.bad_request(f'invalid characters with in the realm name (\'/\' and \' \') are not valid characters')
            return 201, CrudHelper.create(Realm, payload)

        @api.put('/realm/{id}', response={200: RealmSchemaOut, **default_errors},
                 tags=['Realm'], summary='creates a new record')
        def put(request: HttpRequest, payload: RealmSchemaIn, id: str):
            if payload.name.find('/') > -1 or payload.name.find(' ') > -1:
                raise CustomAPIException.bad_request(f'invalid characters with in the realm name (\'/\' and \' \') are not valid characters')
            return CrudHelper.update(Realm, payload, id)
