from django.contrib import admin

# Register your models here.
from hardware.models import Rack, Server

class RackAdmin(admin.ModelAdmin):
    list_display=('name','manager')

class ServerAdmin(admin.ModelAdmin):
    list_display=('number','manager','company','product','rack','conf')

admin.site.register(Rack, RackAdmin)
admin.site.register(Server, ServerAdmin)
