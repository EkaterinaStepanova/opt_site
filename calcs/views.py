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

from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404

#reg form
from django.views.generic.edit import CreateView
from calcs.forms import MeasureForm

#minimization
from calcs.minimization import minimize

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

    measure_name = AllValuesFilter(name='measure__name')

    class Meta:
        model = Measure
        fields = (
            'from_measure_date',
            'to_measure_date',
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
        'method',
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


class MeasureDetail(generics.RetrieveAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-detail'

    renderer_classes = (TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer)
    template_name = 'calcs/measure_detail.html'

    def get_object(self, pk):
        try:
            return Measure.objects.get(pk=pk)
        except Measure.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        measure = self.get_object(pk)
        serializer = MeasureSerializer(measure)
        return Response({ 'serializer': serializer, 'measure': measure })


from django.shortcuts import redirect 
class MeasureCreate(generics.ListCreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-create'

    renderer_classes = (TemplateHTMLRenderer, BrowsableAPIRenderer)
    template_name = 'calcs/measure_create.html'

    def post(self, request, *args, **kwargs):
        form = MeasureForm(request.POST)
        if form.is_valid():
            measure = form.save()
            measure.save()
            serializer = MeasureSerializer(measure, data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                #celery!!!
                minimize_result = minimize(measure)
                minimize_result.save()
                print(measure.get_method())

                return redirect('/measure/', request=request)
        # !TODO Show error message!
        return redirect('/measure/create', request=request)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'measure': reverse(MeasureList.name, request=request),
            })


