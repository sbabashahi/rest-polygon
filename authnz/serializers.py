import os

from django.core.validators import RegexValidator
from django.db import transaction
from django.conf import settings
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework import serializers

from authnz.models import Profile
from utilities import utilities


phone_regex = RegexValidator(regex=r'^\d{12}$',
                             message=_('Phone number must be entered in the format:'
                                       " '989137866088'. 12 digits allowed."))


class RegisterWithEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8, max_length=30)

    def validate_password(self, password):
        if not any(ch.isdigit() for ch in password):
            raise exceptions.ValidationError(detail=_('Password must contain digit.'))
        if not any(ch.isalpha() for ch in password):
            raise exceptions.ValidationError(detail=_('Password must contain alpha.'))
        return password


class LoginEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8, max_length=30)


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=50, required=False)
    email = serializers.EmailField(max_length=50, required=False)
    phone_number = serializers.CharField(validators=[phone_regex], required=False)
    language = serializers.ChoiceField(choices=settings.LANGUAGE_CHOICES, required=False)
    currency = serializers.ChoiceField(choices=settings.CURRENCY_CHOICES, required=False)

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.profile.name = validated_data.get('name', instance.profile.name)
        instance.profile.phone_number = validated_data.get('phone_number', instance.profile.phone_number)
        instance.profile.language = validated_data.get('language', instance.profile.language)
        instance.profile.currency = validated_data.get('currency', instance.profile.currency)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def to_representation(self, instance):
        instance.name = instance.profile.name
        instance.phone_number = instance.profile.phone_number
        instance.language = instance.profile.language
        instance.currency = instance.profile.currency
        instance = super().to_representation(instance)
        return instance
