from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import TokenProxy

from gtfs.admin import FeedInline

from .models import MaasOperator, Permission, TicketingSystem, TransportServiceProvider


class PermissionInline(admin.TabularInline):
    model = Permission
    extra = 0


@admin.register(MaasOperator)
class MaasOperatorAdmin(admin.ModelAdmin):
    inlines = (PermissionInline,)
    fields = ["name", "identifier", "users"]

    # Remove users field if not superuser
    def get_fields(self, request, obj):
        fields = super().get_fields(request, obj)
        fields = fields.copy()
        if not request.user.is_superuser:
            if "users" in fields:
                fields.remove("users")
                return fields
        return fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(users=request.user)
        return qs


@admin.register(TransportServiceProvider)
class TransportServiceProviderAdmin(admin.ModelAdmin):
    inlines = (PermissionInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(users=request.user.id)
        return qs

    # Remove users field if not superuser
    def get_fields(self, request, obj):
        fields = super().get_fields(request, obj)
        fields = fields.copy()
        if not request.user.is_superuser:
            if "users" in fields:
                fields.remove("users")
                return fields
        return fields


@admin.register(TicketingSystem)
class TicketingSystemAdmin(admin.ModelAdmin):
    inlines = (FeedInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(users=request.user.id)
        return qs

    # Remove users field if not superuser
    def get_fields(self, request, obj):
        fields = super().get_fields(request, obj)
        fields = fields.copy()
        if not request.user.is_superuser:
            if "users" in fields:
                fields.remove("users")
                return fields
        return fields


class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(id=request.user.id)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields["is_superuser"].disabled = True
            form.base_fields["is_staff"].disabled = True
            form.base_fields["is_active"].disabled = True
            form.base_fields["user_permissions"].disabled = True
            form.base_fields["groups"].disabled = True
        return form


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CustomTokenAdmin(TokenAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user_id=request.user.id)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields["user"].queryset = User.objects.filter(id=request.user.id)
        return form


admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, CustomTokenAdmin)
