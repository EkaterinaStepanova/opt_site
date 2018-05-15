from rest_framework import serializers
from calcs.models import Measure
from django.contrib.auth.models import User


class MeasureSerializer(serializers.HyperlinkedModelSerializer):
    # We just want to display the owner username (read-only)
    owner = serializers.ReadOnlyField(source='owner.username')

    #client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='name')

    class Meta:
        model = Measure
        #depth = 4
        fields = (
                'url',
                'name',
                'date', 
                'owner',
                'result_exist',
                #'client',
                #'measure'
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