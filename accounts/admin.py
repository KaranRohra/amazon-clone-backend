from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from . import models


class PhoneInline(admin.StackedInline):
    model = models.Phone
    extra = 2


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','country', 'state', 'city')
    search_fields = ('user__email',)
    inlines = (PhoneInline,)


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ('email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
