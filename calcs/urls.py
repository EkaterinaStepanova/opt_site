from django.conf.urls import url, include
from django.urls import path

from calcs import views

from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^measure/$', 
        views.MeasureList.as_view(),
        name=views.MeasureList.name),
    url(r'^measure/(?P<pk>[0-9]+)/$', 
        views.MeasureDetail.as_view(),
        name=views.MeasureDetail.name),
    url(r'^measure/create/$', 
        views.MeasureCreate.as_view(),
        name=views.MeasureCreate.name),

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

#urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns +=[
        url(r'^static/(?P<path>.*)$',
            serve, { 'document_root' : 
            settings.MEDIA_ROOT, }),
    ]
