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


class UserManager(generics.RetrieveAPIView):

    def sign_up(self, request, action):
        self.template_name = 'calcs/user_list.html'  


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

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'calcs/user_list.html'  

    def get(self, request):
        queryset = User.objects.all()
        return Response({'users': queryset})



class UserDetail(generics.RetrieveAPIView):
#class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
     
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAdminUser,
        )

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'calcs/user_detail.html'

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        return Response({'user': user})

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

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAdminUser,
        IsOwnerOrReadOnly,     
        )

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
            'user': reverse(UserList.name, request=request),
            'measure': reverse(MeasureList.name, request=request),
            })


