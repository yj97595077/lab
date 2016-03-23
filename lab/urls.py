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
    url(r'^home/', home),
    url(r'^accounts/login/', login),
    url(r'^accounts/logout/', logout),
    url(r'^server/', server),
    url(r'^servers/serveradd/', server_add),
    url(r'^servers/edit/(?P<id>[\d]+)$',server_edit),
    url(r'^servers/delete/(?P<id>[\d]+)$', server_delete),
]
