from typing import Optional, Any

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.security import django_auth, HttpBasicAuth

from chad_auth_api.rest import exception_handler
from chad_auth_api.rest.client import ClientResource
from chad_auth_api.rest.realm import RealmResource
from chad_auth_api.rest.role import RoleResource
from chad_auth_api.rest.user import UserResource


class ApiBasicAuth(HttpBasicAuth):

    def authenticate(self, request: HttpRequest, username: str, password: str) -> Optional[Any]:
        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            return user.username
        else:
            return None


api = NinjaAPI(csrf=True, auth=[django_auth, ApiBasicAuth()], urls_namespace='api')

exception_handler.register(api)

RealmResource(api)
RoleResource(api)
UserResource(api)
ClientResource(api)
