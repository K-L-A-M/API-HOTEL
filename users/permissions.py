from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import TypeUser


class IsOwnerOrEmployeeOrManagerOrAdministratorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj:
            return True
        return request.user.is_authenticated and (request.user.type_user == TypeUser.EMPLOYEE or request.user.type_user == TypeUser.MANAGER or request.user.type_user == TypeUser.ADMIN)


class IsGuestPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type_user == TypeUser.USER


class IsEmployeePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type_user == TypeUser.EMPLOYEE


class IsManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type_user == TypeUser.MANAGER


class IsAdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type_user == TypeUser.ADMIN


class IsUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user or request.method in SAFE_METHODS


class IsAnyUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsEmployeeOrManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.type_user == TypeUser.EMPLOYEE or request.user.type_user == TypeUser.MANAGER)


class IsManagerOrAdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.type_user == TypeUser.MANAGER or request.user.type_user == TypeUser.ADMIN)


class IsEmployeeOrManagerOrAdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.type_user == TypeUser.EMPLOYEE or request.user.type_user == TypeUser.MANAGER or request.user.type_user == TypeUser.ADMIN)
