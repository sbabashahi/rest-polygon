from django.utils.translation import ugettext as _
from rest_framework import permissions

from utilities.exceptions import CustomException
from geoapp.models import Geo


class SuperUserPermission(permissions.BasePermission):
    """
    Global permission Super user
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


def check_perm_owner_update(request, instance):
    if request.user.is_superuser:
        return True
    if isinstance(instance, Geo) and instance.user == request.user:
        return True
    else:
        raise CustomException(detail=_('No Permission to update'), code=403)


def check_delete_permission(request, instance):
    if request.user.is_superuser:
        return True
    if isinstance(instance, Geo) and instance.user == request.user:
        return True
    else:
        raise CustomException(detail=_('No Permission to delete'), code=403)


def pagination_permission(user, size, index, allowed_size=50):
    if user.is_staff:
        return size, index
    else:
        return size if size < allowed_size else allowed_size, index
