import uuid

from ninja import schema


class RealmSchemaIn(schema.Schema):
    name: str


class RealmSchemaOut(schema.Schema):
    id: uuid.UUID
    name: str
