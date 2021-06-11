from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from . import models


class AddressInline(admin.StackedInline):
    model = models.Address
    extra = 1


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    ordering = ('email',)
    inlines = [AddressInline]
