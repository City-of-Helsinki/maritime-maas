from rest_framework import permissions


class IsMaasOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Allow only MaaS operators to proceed further.
        """
        user = request.user

        if not user.is_authenticated:
            return False

        if user.maas_operators.exists():
            return True

        return False
