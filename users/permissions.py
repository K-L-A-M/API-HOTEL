from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import TypeUser


class IsGuestPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == TypeUser.USER


class IsEmployeePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == TypeUser.EMPLOYEE


class IsManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == TypeUser.MANAGER


class IsAdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == TypeUser.ADMIN


class IsUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user or request.method in SAFE_METHODS


class IsAnyUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsEmployeeOrManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.user_type == TypeUser.EMPLOYEE or request.user.user_type == TypeUser.MANAGER)


class IsManagerOrAdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.user_type == TypeUser.MANAGER or request.user.user_type == TypeUser.ADMIN)


class IsEmployeeOrManagerOrAdministratorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.user_type == TypeUser.EMPLOYEE or request.user.user_type == TypeUser.MANAGER or request.user.user_type == TypeUser.ADMIN)
