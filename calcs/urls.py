from django.conf.urls import url
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


    url(r'^$',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name),
]