from chad_auth_api.models import Client, ClientRole, Role
from chad_auth_api.rest.exception_handler import CustomAPIException
from chad_auth_api.rest.helper import *
from chad_auth_api.schemas.client import ClientSchemaOut, ClientSchemaIn


class ClientResource(object):

    def __init__(self, api: NinjaAPI):
        register(
            {
                PATH: '/client', MODEL_NAME: Client, SCHEMA_OUT: ClientSchemaOut, SCHEMA_IN: ClientSchemaIn,
                ALLOW_CREATE: False, ALLOW_UPDATE: False
            },
            api
        )

        @api.post('/client', response={201: ClientSchemaOut, **default_errors},
                  tags=['Client'], summary='creates a new record')
        def post(request: HttpRequest, payload: ClientSchemaIn):
            existing_client: Client = Client.objects.filter(client_id=payload.client_id, realm_id=payload.realm_id).first()
            if existing_client is not None:
                raise CustomAPIException.bad_request(f'for the realm "{existing_client.realm.name}" is already a client with the client_id {existing_client.client_id} registered')
            return 201, CrudHelper.create(Client, payload)

        @api.put('/client/{id}', response={200: ClientSchemaOut, **default_errors},
                 tags=['Client'], summary='creates a new record')
        def put(request: HttpRequest, payload: ClientSchemaIn, id: str):
            existing_client: Client = Client.objects.filter(client_id=payload.client_id, realm_id=payload.realm_id).first()
            if existing_client is not None and str(existing_client.id) != id:
                raise CustomAPIException.bad_request(f'for the realm "{existing_client.realm.name}" is already a client with the client_id {existing_client.client_id} registered')
            return CrudHelper.update(Client, payload, id)

        @api.put('/client/{id}/roles', response={200: List[str], **default_errors},
                 tags=['Client'], summary='update a clients roles')
        def put_role(request: HttpRequest, roles: List[str], id: str):
            client = get_object_or_404(Client, id=id)
            existing_client_roles = ClientRole.objects.filter(client_id=id)
            for client_role in existing_client_roles:
                if client_role.name not in roles:
                    client_role.delete()
                else:
                    roles.remove(client_role.name)

            existing_roles = [role for role in Role.objects.filter(name__in=roles, realm_id=client.realm.id)]
            for role in roles:
                if role not in [existing_role.name for existing_role in existing_roles]:
                    existing_roles.append(Role.objects.create(name=role, realm_id=client.realm.id))

            for existing_role in existing_client_roles:
                ClientRole.objects.create(client_id=id, role_id=existing_role.id)

            return [role.name for role in existing_roles]
