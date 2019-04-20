from django.utils.translation import ugettext as _
from rest_framework import generics

from utilities import permissions
from utilities.responses import SuccessResponse, ErrorResponse
from utilities.exceptions import CustomException
from utilities.transactions import instance_remover


class DeleteView(generics.DestroyAPIView):
    """
    Delete instance
    """
    def delete(self, request, id, *args, **kwargs):
        try:
            instance = self.model.objects.get(id=id)
            permissions.check_delete_permission(request, instance)
            instance_remover(instance)
            data = {}
            return SuccessResponse(data).send()
        except self.model.DoesNotExist as d:
            return ErrorResponse(message=_('Instance does not exist.'), status=404).send()
        except CustomException as c:
            return ErrorResponse(message=c.detail, status=c.status_code).send()
