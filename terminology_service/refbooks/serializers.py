from rest_framework import serializers
from .models import Refbook, RefbookVersion, RefbookElement


class RefbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refbook
        fields = ['id', 'code', 'name']


class RefbookVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefbookVersion
        fields = ['id', 'refbook', 'version', 'start_date']


class RefbookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefbookElement
        fields = ['id', 'version', 'code', 'value']
