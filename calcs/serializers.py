from rest_framework import serializers
from calcs.models import Measure
from django.contrib.auth.models import User


class MeasureSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Measure
        fields = ( 
            'url'
            'name', 

            'bottom_border', 
            'upper_border', 
            'r', 
            'epsilon', 
            'function',

            'iterations_number',
            'function_minimum',
            'arg_minimum',

            'date',  
            'owner',      
            )


class UserMeasureSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Measure
        fields = (
            'url',
            'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    measure = UserMeasureSerializer(many=True, read_only=True)
    #measure = serializers.SlugRelatedField(queryset=Measure.objects.all(), slug_field='measure')

    class Meta:
        model = User
        fields = (
            'url', 
            'pk',
            'username',
            'measure')    

