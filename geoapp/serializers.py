import json

from django.db import transaction
from rest_framework import serializers
from django.contrib.gis.geos import Polygon, Point, LinearRing

from geoapp.models import Geo


class GeoSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    poly = serializers.ListField(child=serializers.ListField(child=serializers.FloatField(), max_length=2))
    name = serializers.CharField(max_length=50)
    price = serializers.FloatField()

    @transaction.atomic
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['polygon'] = Polygon(validated_data.pop('poly'))
        geo = Geo(**validated_data)
        geo.save()
        return geo

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.name = validated_data.get('name', instance.name)
        instance.polygon = Polygon(validated_data.get('polygon', instance.polygon))
        instance.save()
        return instance

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data

    def to_representation(self, instance):
        polygon = []
        for item in instance.polygon:
            for point in item:
                polygon.append(list(point))
        # json.loads(instance.polygon.geojson)
        # import pdb;pdb.set_trace()
        instance.poly = json.loads(instance.polygon.geojson)['coordinates'][0]
        instance = super().to_representation(instance)
        return instance
