from django.conf.urls import url, include
from django.urls import path
from calcs import views


urlpatterns = [
    url(r'^measure/$', 
        views.MeasureList.as_view(),
        name=views.MeasureList.name),
    url(r'^measure/(?P<pk>[0-9]+)/$', 
        views.MeasureDetail.as_view(),
        name=views.MeasureDetail.name),

    url(r'^user/$',
        views.UserList.as_view(),
        name=views.UserList.name),
    url(r'^user/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name=views.UserDetail.name),
    # url(r'^sign-up/(?P<pk>[0-9]+)/$',
    #      views.UserManager.as_view(action='sign-up'),
    #      name=views.UserManager.name),
    # path('user/', include('django.contrib.auth.urls')),
    #url(r'^user/', include('django.contrib.auth.urls')),

    #url(r'^signup/$', views.signup, name='signup'),


    url(r'^$',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name),
]