from rest_framework import serializers
from calcs.models import Measure
from django.contrib.auth.models import User


class MeasureSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Measure
        fields = ( 
            'name', 
            'bottom_border', 
            'upper_border', 
            'r', 
            'epsilon', 
            )

