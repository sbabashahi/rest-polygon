from rest_framework import decorators
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utilities.tools import create, delete, list_result, update
from utilities.utilities import CUSTOM_PAGINATION_SCHEMA
from utilities import permissions
from geoapp.models import Geo
from geoapp.serializers import GeoSerializer


@decorators.authentication_classes([JSONWebTokenAuthentication])
@decorators.permission_classes([IsAuthenticated])
class GeoCreateView(create.CreateView):
    serializer_class = GeoSerializer
    model = Geo


@decorators.authentication_classes([JSONWebTokenAuthentication])
@decorators.permission_classes([IsAuthenticated])
@decorators.schema(CUSTOM_PAGINATION_SCHEMA)
class GeoListView(list_result.ListView):
    serializer_class = GeoSerializer
    model = Geo


@decorators.authentication_classes([JSONWebTokenAuthentication])
@decorators.permission_classes([IsAuthenticated])
class GeoUpdateView(update.UpdateView):
    serializer_class = GeoSerializer
    model = Geo


@decorators.authentication_classes([JSONWebTokenAuthentication])
@decorators.permission_classes([IsAuthenticated])
class GeoDeleteView(delete.DeleteView):
    serializer_class = GeoSerializer
    model = Geo
