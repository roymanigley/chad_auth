from chad_auth_api.models import User, UserRole, Role
from chad_auth_api.rest.exception_handler import CustomAPIException
from chad_auth_api.rest.helper import *
from chad_auth_api.schemas.user import UserSchemaOut, UserSchemaIn


class UserResource(object):

    def __init__(self, api: NinjaAPI):
        register(
            {
                PATH: '/user', MODEL_NAME: User, SCHEMA_OUT: UserSchemaOut, SCHEMA_IN: UserSchemaIn,
                ALLOW_CREATE: False, ALLOW_UPDATE: False
            },
            api
        )

        @api.post('/user', response={201: UserSchemaOut, **default_errors},
                  tags=['User'], summary='creates a new record')
        def post(request: HttpRequest, payload: UserSchemaIn):
            existing_user: User = User.objects.filter(username=payload.username, realm_id=payload.realm_id).first()
            if existing_user is not None:
                raise CustomAPIException.bad_request(
                    f'for the realm "{existing_user.realm.name}" is already a user with the username {existing_user.username} registered')
            payload.password = User.hash_password(payload.password)
            return 201, CrudHelper.create(User, payload)

        @api.put('/user/{id}', response={200: UserSchemaOut, **default_errors},
                 tags=['User'], summary='creates a new record')
        def put(request: HttpRequest, payload: UserSchemaIn, id: str):
            existing_user: User = User.objects.filter(username=payload.username, realm_id=payload.realm_id).first()
            if existing_user is not None and str(existing_user.id) != id:
                raise CustomAPIException.bad_request(
                    f'for the realm "{existing_user.realm.name}" is already a user with the username {existing_user.username} registered')
            payload.password = User.hash_password(payload.password)
            return CrudHelper.update(User, payload, id)

        @api.put('/user/{id}/roles', response={200: List[str], **default_errors},
                 tags=['User'], summary='update a users roles')
        def put_role(request: HttpRequest, roles: List[str], id: str):
            user = get_object_or_404(User, id=id)
            existing_user_roles = UserRole.objects.filter(user_id=id)
            for user_role in existing_user_roles:
                if user_role.name not in roles:
                    user_role.delete()
                else:
                    roles.remove(user_role.name)

            existing_roles = [role for role in Role.objects.filter(name__in=roles, realm_id=user.realm.id)]
            for role in roles:
                if role not in [existing_role.name for existing_role in existing_roles]:
                    existing_roles.append(Role.objects.create(name=role, realm_id=user.realm.id))

            for existing_role in existing_user_roles:
                UserRole.objects.create(user_id=id, role_id=existing_role.id)

            return [role.name for role in existing_roles]
