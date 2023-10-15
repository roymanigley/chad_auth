from typing import List

from django.db import models
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja import schema

from chad_auth_api.rest.exception_handler import default_errors

PATH = 'path'
MODEL_NAME = 'model_name'
SCHEMA_OUT = 'schema_out'
SCHEMA_IN = 'schema_in'

ALLOW_GET_ALL = 'allow_get_all'
ALLOW_GET_BY_ID = 'allow_get_by_id'
ALLOW_CREATE = 'allow_create'
ALLOW_UPDATE = 'allow_update'
ALLOW_DELETE = 'allow_delete'


class CrudHelper(object):

    @staticmethod
    def get_all(model_class: models.Model):
        return model_class.objects.all()

    @staticmethod
    def get_by_id(model_class: models.Model, id: str):
        return get_object_or_404(model_class, id=id)

    @staticmethod
    def create(model_class: models.Model, payload: schema.Schema):
        return model_class.objects.create(**payload.__dict__)

    @staticmethod
    def update(model_class: models.Model, payload: schema.Schema, id: str):
        record = get_object_or_404(model_class, id=id)
        for attr, val in payload.dict().items():
            setattr(record, attr, val)
        record.save()
        return record

    @staticmethod
    def delete(model_class: models.Model, id: str):
        get_object_or_404(model_class, id=id).delete()


def register(crud_entity: dict, api: NinjaAPI):
    if ALLOW_GET_ALL not in crud_entity.keys():
        crud_entity[ALLOW_GET_ALL] = True
    if ALLOW_GET_BY_ID not in crud_entity.keys():
        crud_entity[ALLOW_GET_BY_ID] = True
    if ALLOW_CREATE not in crud_entity.keys():
        crud_entity[ALLOW_CREATE] = True
    if ALLOW_UPDATE not in crud_entity.keys():
        crud_entity[ALLOW_UPDATE] = True
    if ALLOW_DELETE not in crud_entity.keys():
        crud_entity[ALLOW_DELETE] = True

    if crud_entity[ALLOW_GET_ALL]:
        @api.get(crud_entity[PATH], response={200: List[crud_entity[SCHEMA_OUT]], **default_errors},
                 tags=[crud_entity[PATH][1:].title()], summary='returns all records')
        def get_all(request: HttpRequest):
            return CrudHelper.get_all(crud_entity[MODEL_NAME])

    if crud_entity[ALLOW_GET_BY_ID]:
        @api.get(f'{crud_entity[PATH]}/{{id}}', response={200: crud_entity[SCHEMA_OUT], **default_errors},
                 tags=[crud_entity[PATH][1:].title()],
                 summary='returns a single record by id or 404')
        def get_by_id(request: HttpRequest, id: str):
            return CrudHelper.get_by_id(crud_entity[MODEL_NAME], id)

    if crud_entity[ALLOW_CREATE]:
        @api.post(crud_entity[PATH], response={201: crud_entity[SCHEMA_OUT], **default_errors},
                  tags=[crud_entity[PATH][1:].title()], summary='creates a new record')
        def post(request: HttpRequest, payload: crud_entity[SCHEMA_IN]):
            return 201, CrudHelper.create(crud_entity[MODEL_NAME], payload)

    if crud_entity[ALLOW_UPDATE]:
        @api.put(f'{crud_entity[PATH]}/{{id}}', response={200: crud_entity[SCHEMA_OUT], **default_errors},
                 tags=[crud_entity[PATH][1:].title()],
                 summary='updates a record or returns 404 if the id is not found in the database')
        def put(request: HttpRequest, payload: crud_entity[SCHEMA_IN], id: str):
            return CrudHelper.update(crud_entity[MODEL_NAME], payload, id)

    if crud_entity[ALLOW_DELETE]:
        @api.delete(f'{crud_entity[PATH]}/{{id}}', response={203: None, **default_errors},
                    tags=[crud_entity[PATH][1:].title()], summary='deletes the record or returns 404 if the record does not exist')
        def delete(request: HttpRequest, id: str):
            return CrudHelper.delete(crud_entity[MODEL_NAME], id)