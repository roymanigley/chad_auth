import uuid

from ninja import schema

from chad_auth_api.schemas.user import RealmSchemaOut


class RoleSchemaIn(schema.Schema):
    name: str
    realm_id: uuid.UUID


class RoleSchemaOut(schema.Schema):
    id: uuid.UUID
    name: str
    realm: RealmSchemaOut
