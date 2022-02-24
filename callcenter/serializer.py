from rest_framework import serializers
from .models import *


class FilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uploades
        fields = '__all__'


class CallerSerializer(serializers.ModelSerializer):

    uploades_set = FilesSerializer(many=True)

    class Meta:
        model = Caller
        fields = '__all__'

