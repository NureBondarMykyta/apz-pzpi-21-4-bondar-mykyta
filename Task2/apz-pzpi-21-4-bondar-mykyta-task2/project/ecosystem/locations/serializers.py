# serializers.py

from rest_framework import serializers
from .models import Location, Parameter, MonitoringData


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['parameter_name', 'unit', 'weight']


class MonitoringDataSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer()

    class Meta:
        model = MonitoringData
        fields = ['parameter', 'value']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'country', 'city', 'location_type']




