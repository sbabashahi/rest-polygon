from django.core.exceptions import FieldError
from rest_framework import generics
from querystring_parser import parser

from utilities import responses
from utilities import permissions


class ListView(generics.ListAPIView):
    """
    list of items for admins api

    with order by, size, index
    """

    def get(self, request, *args, **kwargs):
        try:
            arguments = parser.parse(request.GET.urlencode())

            size = int(arguments.pop('size', 20))
            index = int(arguments.pop('index', 0))
            size, index = permissions.pagination_permission(request.user, size, index)
            size = index + size

            sort = None
            if arguments.get('order_by'):
                sort = arguments.pop('order_by')

            result = self.model.objects.filter(**arguments)
            if sort:
                result = result.order_by(sort)
            result = result.all()
            total = len(result)
            result = result[index:size]
            data = self.get_serializer(result, many=True)
            return responses.SuccessResponse(data.data, index=index, total=total).send()
        except FieldError as e:
            return responses.ErrorResponse(message=str(e)).send()


class UserListView(generics.ListAPIView):
    """
    list of items for admins api

    with order by, size, index
    """

    def get(self, request, *args, **kwargs):
        try:
            arguments = parser.parse(request.GET.urlencode())
            size = int(arguments.pop('size', 20))
            index = int(arguments.pop('index', 0))
            size, index = permissions.pagination_permission(request.user, size, index)
            size = index + size

            sort = None
            if arguments.get('order_by'):
                sort = arguments.pop('order_by')

            result = self.model.objects.filter(**arguments)
            if sort:
                result = result.order_by(sort)

            result = result.all()
            total = len(result)
            result = result[index:size]
            data = self.get_serializer(result, many=True)
            return responses.SuccessResponse(data.data, index=index, total=total).send()
        except FieldError as e:
            return responses.ErrorResponse(message=str(e)).send()
