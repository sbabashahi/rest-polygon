import hashlib

from django.db import transaction
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import decorators
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

from authnz import serializers as authnz_serializers
from authnz import transactions
from authnz.models import Profile
from utilities import responses, utilities, exceptions as authnz_exceptions,permissions


@decorators.authentication_classes([])
@decorators.permission_classes([])
class RegisterWithEmailView(generics.CreateAPIView):
    """
    Register with email and password pass min len is 8 and need alpha and numeric max len is 30
    """
    serializer_class = authnz_serializers.RegisterWithEmailSerializer

    def post(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                email = serialized_data.data['email'].lower()
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist as e:
                    user = None

                if user:
                    raise authnz_exceptions.CustomException(detail=_('This email is registered before.'))
                else:
                    password = serialized_data.data['password']
                    user = transactions.register_user_with_email_and_password(email, password)
                    return responses.SuccessResponse().send()
        except authnz_exceptions.CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        except exceptions.ValidationError as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@decorators.authentication_classes([])
@decorators.permission_classes([])
class LoginEmailView(generics.CreateAPIView):
    """
    Login with email and password
    """
    serializer_class = authnz_serializers.LoginEmailSerializer

    def post(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid(raise_exception=True):
                email = serialized_data.data['email'].lower()
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    raise authnz_exceptions.CustomException(detail=_('Username or Password is invalid.'))

                if user.check_password(serialized_data.data['password']):
                    if user.is_active:
                        payload = jwt_payload_handler(user)  # todo: Is deprecated
                        jwt_token = utilities.jwt_response_payload_handler(jwt_encode_handler(payload), user=user)
                        return responses.SuccessResponse(jwt_token).send()
                    else:
                        raise authnz_exceptions.CustomException(detail=_('This user is inactive, contact us.'))
                else:
                    raise authnz_exceptions.CustomException(detail=_('Username or Password is invalid.'))
        except authnz_exceptions.CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        except exceptions.ValidationError as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@decorators.authentication_classes([JSONWebTokenAuthentication])
@decorators.permission_classes([IsAuthenticated])
class RefreshTokenView(generics.RetrieveAPIView):
    """
    Refresh JWT token
    """
    def get(self, request):
        try:
            if request.user.is_active:
                payload = jwt_payload_handler(request.user)  # todo: Is deprecated
                jwt_token = utilities.jwt_response_payload_handler(jwt_encode_handler(payload),
                                                                   user=request.user)
                return responses.SuccessResponse(jwt_token).send()
            else:
                raise authnz_exceptions.CustomException(detail=_('This user is inactive, contact us.'))

        except authnz_exceptions.CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@decorators.authentication_classes([JSONWebTokenAuthentication])
@decorators.permission_classes([IsAuthenticated])
class UpdateUserProfileView(generics.UpdateAPIView):
    """
    Update user profile

    """
    serializer_class = authnz_serializers.UserSerializer
    model = User

    def patch(self, request):
        try:
            serialize_data = self.get_serializer(request.user, data=request.data, partial=True)
            if serialize_data.is_valid(raise_exception=True):
                try:
                    self.perform_update(serialize_data)
                except Exception as e:
                    raise e
                serialize_data = self.get_serializer(request.user)
                return responses.SuccessResponse(serialize_data.data).send()

        except exceptions.ValidationError as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        except Exception as e:
            return responses.ErrorResponse(message=str(e)).send()

    def put(self, request):
        try:
            serialize_data = self.get_serializer(request.user, data=request.data)
            if serialize_data.is_valid(raise_exception=True):
                try:
                    self.perform_update(serialize_data)
                except Exception as e:
                    raise e
                serialize_data = self.get_serializer(request.user)
                return responses.SuccessResponse(serialize_data.data).send()

        except exceptions.ValidationError as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
        except Exception as e:
            return responses.ErrorResponse(message=str(e)).send()
