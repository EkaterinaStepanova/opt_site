from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from calcs.models import Measure
from calcs.serializers import MeasureSerializer, UserSerializer

from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer
from rest_framework.throttling import ScopedRateThrottle

from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter
from django_filters.rest_framework import FilterSet 

from django.http import Http404

#reg form
from django.views.generic.edit import CreateView
from calcs.forms import MeasureForm, UserCreateForm, UserLoginForm
from django.contrib import messages 
from django.conf import settings

#minimization
from calcs.minimization import minimize

#pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

#user
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

#permissions
from calcs.permissions import IsOwnerOrStaff


# !TODO /welcome/ page 

class UserCreate(generics.CreateAPIView):
    model = User
    fields = ['username', 'password']
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'calcs/registration.html' 
    name = 'user-create'
    serializer_class = UserSerializer

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super(UserCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/measure/', request=request) 

        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST["password"])
            user.save()
            serializer = UserSerializer(user, data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                return redirect('/measure/', request=request)
        # !TODO Show error message!
        messages.error(request, str(form['username'].errors)+str(form['password'].errors))
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/measure/', request=request) 
        return render(request, self.template_name)


class UserLogin(APIView):
    model = User
    fields = ['username', 'password']
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'calcs/login.html' 
    name = 'user-login'
    serializer_class = UserSerializer

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super(UserCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/measure/', request=request) 

        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user = authenticate(username=user.username, password=user.password)
            if user is not None:
                login(request, user)
                serializer = UserSerializer(user, data=request.data, context={'request': request})
                if serializer.is_valid(raise_exception=True):
                    return redirect('/measure/', request=request)
                else:
                    raise Http404("Can not get serializer")

        messages.error(request, str(form['username'].errors)+str(form['password'].errors))
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/measure/', request=request) 
        return render(request, self.template_name)


class UserLogout(generics.RetrieveAPIView):
    model = User
    fields = ['username', 'password']
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'calcs/base.html' 
    name = 'user-logout'
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)


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


class MeasureList(generics.ListAPIView):  
    serializer_class = MeasureSerializer
    name = 'measure-list'
    queryset = Measure.objects.all()

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

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/', request=request)
        if request.user.is_staff:
            print('is_staff')
            self.queryset = Measure.objects.all()
        else:
            print(str(request.user))
            self.queryset = Measure.objects.all().filter(owner=str(request.user))
            print(self.queryset)
        paginator = Paginator(self.queryset, settings.REST_FRAMEWORK['PAGE_SIZE']) # Show 25 contacts per page
        page = request.GET.get('page')
        measures = paginator.get_page(page)
        return render(request, self.template_name, {'measures': measures})


class MeasureDetail(generics.RetrieveAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-detail'

    renderer_classes = (TemplateHTMLRenderer, BrowsableAPIRenderer, JSONRenderer)
    template_name = 'calcs/measure_detail.html'

    # permission_classes = (
    #     IsOwnerOrStaff,   
    #     permissions.IsAuthenticated,  
    #     )

    def get_object(self, pk):
        try:
            return Measure.objects.get(pk=pk)
        except Measure.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):      
        measure = self.get_object(pk)
        if not (measure.owner == request.user or request.user.is_staff):
            return redirect('/measure/', request=request)
        serializer = MeasureSerializer(measure)
        return Response({ 'serializer': serializer, 'measure': measure })


class MeasureCreate(generics.CreateAPIView):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    name = 'measure-create'

    renderer_classes = (TemplateHTMLRenderer, BrowsableAPIRenderer)
    template_name = 'calcs/measure_create.html'

    def post(self, request, *args, **kwargs):
        form = MeasureForm(request.POST)
        if form.is_valid():
            measure = form.save()
            measure.owner=self.request.user
            measure.save()
            serializer = MeasureSerializer(measure, data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                #celery!!!
                minimize_result = minimize(measure)
                minimize_result.save()
                return redirect('/measure/', request=request)
        # !TODO Show error message!
        messages.error(request, str(form['function'].errors))
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    renderer_classes = (TemplateHTMLRenderer, BrowsableAPIRenderer)
    template_name = 'calcs/welcome.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
            'measure': reverse(MeasureList.name, request=request),
            'user': reverse(UserCreate.name, request=request),
            })  
        else:
             return Response({
            'measure': reverse(MeasureList.name, request=request),
            })  
        


