"""lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from hardware.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', home),
    url(r'^about/$', about),
    url(r'^accounts/signup/$', signup),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^server/$', server),
    url(r'^server/search/(?P<search>\w+)/(?P<id>\d+)/$', server),
    url(r'^server/search/(?P<search>\w+)/(?P<item>\w+)/$', server),
    url(r'^server/add/$', server_add),
    url(r'^server/edit/(?P<id>\d+)/$',server_edit),
    url(r'^server/delete/(?P<id>\d+)/$', server_delete),
    url(r'^server/detail/(?P<id>\d+)/$', server_detail),
    url(r'^server/ssh/(?P<id>\d+)/$', server_ssh),
    url(r'^switch/$', switch),
    url(r'^switch/search/(?P<search>\w+)/(?P<id>\d+)/$', switch),
    url(r'^switch/search/(?P<search>\w+)/(?P<item>\w+)/$', switch),
    url(r'^switch/add/$', switch_add),
    url(r'^switch/edit/(?P<id>\d+)/$',switch_edit),
    url(r'^switch/delete/(?P<id>\d+)/$', switch_delete),
    url(r'^switch/detail/(?P<id>\d+)/$', switch_detail),
    url(r'^switch/telnet/(?P<id>\d+)/$', switch_telnet),
    url(r'^switch/manage/(?P<id>\d+)/$', switch_manage),
    url(r'^ip/$', ip),
    url(r'^ip/search/(?P<search>\w+)/(?P<id>\d+)/$', ip),
    url(r'^ip/search/(?P<search>\w+)/(?P<item>\w+)/$', ip),
    url(r'^ip/add/$', ip_add),
    url(r'^ip/delete/(?P<id>\d+)/$', ip_delete),
    url(r'^ip/checkbox/delete/$', ip_delete),
]
