# -*- coding: utf-8 -*-

from django.contrib import admin

# Register your models here.
from hardware.models import *

#注册模块，两种方法，第一种的控制更精准
'''
class ServerAdmin(admin.ModelAdmin):
    list_display=('number','manager','company','product',...)

admin.site.register(Server, ServerAdmin)
'''
admin.site.register(Manager)
admin.site.register(Company)
admin.site.register(Rack)
admin.site.register(Server)
