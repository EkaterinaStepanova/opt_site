from rest_framework import serializers
#from calcs.models import MeasureInput
#from calcs.models import MeasureOutput
from calcs.models import Measure
from calcs.models import Client
from calcs.models import ClientMeasure
from django.contrib.auth.models import User

'''
class MeasureInputSerializer(serializers.HyperlinkedModelSerializer):
    pass


class MeasureOutputSerializer(serializers.HyperlinkedModelSerializer):
    pass'''

class UserMeasureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measure
        fields = (
            'url',
            'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    measures = UserMeasureSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'url', 
            'pk',
            'username',
            'measures')      


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
                #'input', #?
                #'output', #?
                'used',
                #'client',
                #'measure'
                )



class ClientSerializer(serializers.HyperlinkedModelSerializer):
    measures = MeasureSerializer(many=True, read_only=True)
    #measures = serializers.SlugRelatedField(queryset=Measure.objects.all(), slug_field='name')
    post = serializers.ChoiceField(
        choices=Client.POST_CHOICES)
    #post_description = serializers.CharField(
    #    source='get_post_display', 
    #    read_only=True)

    class Meta:
        model = Client
        fields = (
            'url',
            'name',
            'post',
            #'post_description',
            'measures',
            )  


class ClientMeasureSerializer(serializers.HyperlinkedModelSerializer):
    # We just want to display the owner username (read-only)
    #owner = serializers.ReadOnlyField(source='owner.username')

    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='name')
    measure = serializers.SlugRelatedField(queryset=Measure.objects.all(), slug_field='name')

    class Meta:
        model = ClientMeasure
        fields = (
                'url',
                'pk',
                #'date', 
                #'owner',
                #'input', #?
                #'output', #?
                #'used',
                'client',
                'measure',
                )

