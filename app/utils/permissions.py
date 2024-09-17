from rest_framework.permissions import BasePermission, DjangoModelPermissions, SAFE_METHODS

from octos.logging import Logger

logger = Logger(__name__).get()


class IsStaff(BasePermission):
    """
    Custom permission to only allow staff users to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_staff


class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class UserVerified(BasePermission):
    """
    Custom permission to only allow users to access the view if their email is verified.
    """

    def has_permission(self, request, view):
        if request.user.email_verified and request.user.is_staff:
            return True
        return False


class EmailNotVerified(BasePermission):
    """
    Custom permission to only allow users to access the view if their email is not verified.
    """

    def has_permission(self, request, view):
        return not request.user.email_verified


class ReadOrAdmin(BasePermission):
    """
    Custom permission to only allow read-only access to the view for non-admin users.
    """

    def has_permission(self, request, view):
        if request.method in ["GET"]:
            return True
        if request.method in ["POST", "PUT", "DELETE"]:
            if request.user.is_authenticated and request.user.is_superuser:
                return True
        return False


class LoginPermission(BasePermission):
    """
    Custom permission to only allow authenticated users to access the view.
    """

    def has_permission(self, request, view):
        if request.method in ["DELETE"]:
            if not request.user.is_authenticated:
                return False
        return True


class NotAuthenticatedPermission(BasePermission):
    """
    Custom permission to only allow not authenticated users to access the view.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return False


class MePermission(BasePermission):
    """
    Custom permission to only allow the authenticated users to access their own profile.
    """

    def has_permission(self, request, view):
        if request.method in ["GET"] and not request.user.is_authenticated:
            return False
        return True


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # only allowed to the owner of the customer profile
        return obj.user == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit or delete an object, but allow read-only access to all users.
    """

    def has_permission(self, request, view):
        # Allow read-only access for everyone
        if request.method in SAFE_METHODS:
            return True

        # Otherwise, only allow access to admin users
        return request.user and request.user.is_staff


class IsAdminOrStaff(BasePermission):
    """
    Custom permission to allow only admin users or staff members to manage purchase orders.
    """

    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)


class NotAuthenticatedOrStaffPermission(BasePermission):
    """
    Custom permission that allows:
    - Unauthenticated users to register as a customer.
    - Staff (admin) users to register new users with roles like 'salesman' or 'delivery'.
    """

    def has_permission(self, request, view):
        # Allow unauthenticated users to register as a customer
        if not request.user.is_authenticated:
            return True

        # If the user is authenticated, check if they are a staff or superuser
        if request.user.is_authenticated and request.user.is_staff:
            return True

        return False


class ModelPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": [],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
