from django.shortcuts import render

# Create your views here.
#from calcs.models import MeasureInput
#from calcs.models import MeasureOutput
from calcs.models import Measure
from calcs.models import Client
from calcs.models import ClientMeasure

from calcs.serializers import MeasureSerializer
from calcs.serializers import ClientSerializer
from calcs.serializers import ClientMeasureSerializer
from calcs.serializers import UserMeasureSerializer
from calcs.serializers import UserSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import filters
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter
from calcs.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import FilterSet 


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class MeasureList(generics.ListCreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
        )
    filter_fields = (
        'name', 
        'date', 
        'used', 
        #'owner',
        #'client'
        )
    search_fields = (
        '^name',
        )
    ordering_fields = (
        'name',
        'date',
        )

    def perform_create(self, serializer):
        #serializer.save(owner=self.request.user)
        serializer.save()

class MeasureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly)


class ClientList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    name = 'client-list'
    filter_fields = (
        'name', 
        'post', 
        )
    search_fields = (
        '^name',
        )
    ordering_fields = (
        'name',
        )


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    name = 'client-detail'


class ClientMeasureListFilter(FilterSet):

    from_measure_date = DateTimeFilter(
        name='measure_date', lookup_expr='gte')
    to_measure_date = DateTimeFilter(
        name='measure_date', lookup_expr='lte')

    client_name = AllValuesFilter(
        name='client__name')
    measure_name = AllValuesFilter(
        name='measure__name')

    class Meta:
        model = ClientMeasure
        fields = (
            'from_measure_date',
            'to_measure_date',
            #player__name will be accessed as player_name
            'client_name',
            #game__name will be accessed as game_name
            'measure_name',
            )



class ClientMeasureList(generics.ListCreateAPIView):
    queryset = ClientMeasure.objects.all()
    serializer_class = ClientMeasureSerializer
    name = 'client-measure-list'
    filter_class = ClientMeasureListFilter
    ordering_fields = (
        'date',
        'name',
        )
'''
    ordering_fields = (
        'from_measure_date',
        'to_measure_date',
        'client_name',
        'measure_name',
        )'''


class ClientMeasureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClientMeasure.objects.all()
    serializer_class = ClientMeasureSerializer
    name = 'client-measure-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'clients': reverse(ClientList.name, request=request),
            'measures': reverse(MeasureList.name, request=request),
            'client-measures': reverse(ClientMeasureList.name, request=request),
            #'users': reverse(UserList.name, request=request),
            })


