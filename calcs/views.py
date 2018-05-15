from django.shortcuts import render

# Create your views here.

from calcs.models import Measure
from django.contrib.auth.models import User

from calcs.serializers import MeasureSerializer
from calcs.serializers import UserMeasureSerializer
from calcs.serializers import UserSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse


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

    permission_classes = (
        permissions.IsAdminUser,
        )

    filter_fields = (
        'username', 
        )
    search_fields = (
        '^username',
        )
    ordering_fields = (
        'username',
        )


class UserDetail(generics.RetrieveAPIView):
#class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAdminUser,
        )


class MeasureListFilter(FilterSet):
    from_measure_date = DateTimeFilter(
        name='measure_date', lookup_expr='gte')
    to_measure_date = DateTimeFilter(
        name='measure_date', lookup_expr='lte')

    owner_username = AllValuesFilter(name='owner__username')

    measure_name = AllValuesFilter(name='measure__name')

    class Meta:
        model = Measure
        fields = (
            'from_measure_date',
            'to_measure_date',
            'owner_username',
            'measure_name',
            )


class MeasureList(generics.ListCreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,     
        )
    #filter_class = MeasureListFilter
    filter_fields = (
        'name', 
        'date', 
        'result_exist', 
        'owner',
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
    template_name = 'calcs/measure_detail.html'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAdminUser,
        IsOwnerOrReadOnly,     
        )


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'user': reverse(UserList.name, request=request),
            'measure': reverse(MeasureList.name, request=request),
            })


