from django.conf.urls import url
from calcs import views


urlpatterns = [
    url(r'^measures/$', 
        views.MeasureList.as_view(),
        name=views.MeasureList.name),
    url(r'^measures/(?P<pk>[0-9]+)/$', 
        views.MeasureDetail.as_view(),
        name=views.MeasureDetail.name),

    url(r'^clients/$', 
        views.ClientList.as_view(),
        name=views.ClientList.name),
    url(r'^clients/(?P<pk>[0-9]+)/$', 
        views.ClientDetail.as_view(),
        name=views.ClientDetail.name),

    url(r'^users/$',
        views.UserList.as_view(),
        name=views.UserList.name),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name=views.UserDetail.name),

    url(r'^client-measures/$', 
        views.ClientMeasureList.as_view(),
        name=views.ClientMeasureList.name),
    url(r'^client-measures/(?P<pk>[0-9]+)/$', 
        views.ClientMeasureDetail.as_view(),
        name=views.ClientMeasureDetail.name),

    url(r'^$',
        views.ApiRoot.as_view(),
        name=views.ApiRoot.name),
]