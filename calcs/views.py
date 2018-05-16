from django.shortcuts import render

# Create your views here.

from calcs.models import Measure
from calcs.serializers import MeasureSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework import permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework import filters
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter

from django_filters.rest_framework import FilterSet 

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.http import Http404

#reg form
from django.views.generic.edit import CreateView

# class UserCreate(CreateView):
#     model = User
#     fields = ['username', password]

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super(AuthorCreate, self).form_valid(form)


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

    #filter_class = MeasureListFilter
    filter_fields = (
        'name', 
        'date', 
        'result_exist', 
        )
    search_fields = (
        '^name',
        )
    ordering_fields = (
        'name',
        'date',
        )

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'calcs/measure_list.html'  

    def get(self, request):
        queryset = Measure.objects.all()
        return Response({'measures': queryset})

    def perform_create(self, serializer):
        #serializer.save(owner=self.request.user)
        serializer.save()


class MeasureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-detail'

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'calcs/measure_detail.html'

    def get_object(self, pk):
        try:
            return Measure.objects.get(pk=pk)
        except Measure.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        measure = self.get_object(pk)
        return Response({'measure': measure})


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'measure': reverse(MeasureList.name, request=request),
            })


