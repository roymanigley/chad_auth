from django.contrib import admin
from django.contrib.admin import ModelAdmin

from chad_auth_api.models import Realm, Client, User


class RealmModel(ModelAdmin):
    list_display = ['name']


class ClientModel(ModelAdmin):
    list_display = ['client_id']


class UserModel(ModelAdmin):
    list_display = ['username']


# Register your models here.
admin.site.register(Realm, RealmModel)
admin.site.register(Client, ClientModel)
admin.site.register(User, UserModel)
