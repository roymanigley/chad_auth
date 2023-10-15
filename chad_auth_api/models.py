import uuid
from hashlib import sha512

from django.db import models


class Realm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=False, blank=False, max_length=100, unique=True)


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=False, blank=False, max_length=100)
    realm = models.ForeignKey(Realm, null=False, on_delete=models.CASCADE)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(null=False, blank=False, max_length=100)
    password = models.CharField(null=False, blank=False, max_length=100)
    realm = models.ForeignKey(Realm, null=False, on_delete=models.CASCADE)

    @staticmethod
    def hash_password(password: str) -> str:
        return sha512(password.encode('utf-8')).hexdigest()


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.CharField(null=False, blank=False, max_length=100)
    client_secret = models.CharField(null=False, blank=False, max_length=100)
    redirect_uris = models.JSONField(null=False)
    realm = models.ForeignKey(Realm, null=False, on_delete=models.CASCADE)


class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, null=False, on_delete=models.CASCADE)


class ClientRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, null=False, on_delete=models.CASCADE)
