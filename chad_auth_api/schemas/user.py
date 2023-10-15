import uuid

from ninja import schema

from chad_auth_api.schemas.realm import RealmSchemaOut


class UserSchemaIn(schema.Schema):
    username: str
    password: str
    realm_id: str


class UserSchemaOut(schema.Schema):
    id: uuid.UUID
    username: str
    realm: RealmSchemaOut
