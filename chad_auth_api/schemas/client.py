import uuid
from typing import List

from ninja import schema

from chad_auth_api.schemas.realm import RealmSchemaOut


class ClientSchemaIn(schema.Schema):
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    realm_id: str


class ClientSchemaOut(schema.Schema):
    id: uuid.UUID
    client_id: str
    client_secret: str
    redirect_uris: List[str]
    realm: RealmSchemaOut
