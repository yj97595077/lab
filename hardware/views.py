from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Rack, Server
from .forms import ServerForm, LoginForm

# Create your views here.

def home(request):
    return render_to_response('hardware/home.html', RequestContext(request))

def login(request):
    if request.method == 'GET':
        loginform = LoginForm()
        return render_to_response('hardware/login.html', RequestContext(request, {'loginform': loginform,}))
    else:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/home')
            else:
                return render_to_response('hardware/login.html', RequestContext(request, {'loginform': loginform,'password_is_wrong':True}))
        else:
            return render_to_response('hardware/login.html', RequestContext(request, {'loginform': loginform,}))

def logout(request):
    auth.logout(request)
    return render_to_response('hardware/logout.html', RequestContext(request))

@login_required
def server(request):
    servers = Server.objects.all()
    return render_to_response('hardware/server.html', RequestContext(request, {'servers': servers}))

@login_required
def server_add(request):
    if request.method == 'GET':
        serverform = ServerForm()
        return render_to_response('hardware/server_add.html', RequestContext(request,{'serverform':serverform}))
    else:
        serverform = ServerForm(request.POST)
        if serverform.is_valid():
            server = Server()
            server.number = serverform.cleaned_data['number']
            server.manager = serverform.cleaned_data['manager']
            server.company = serverform.cleaned_data['company']
            server.product = serverform.cleaned_data['product']
            server.rack = serverform.cleaned_data['rack']
            server.conf = serverform.cleaned_data['conf']
            server.save()
            return render_to_response('hardware/server_add.html', RequestContext(request,{'serverform':serverform}))
        else:
            return render_to_response('hardware/server_add.html', RequestContext(request,{'serverform':serverform}))

@login_required
def server_edit(request, id):
    if request.method == 'GET':
        server = Server.objects.get(id=id)
        serverform = ServerForm(initial = { "number": server.number, "manager": server.manager, "company": server.company, "product": server.product, "rack": server.rack, "conf": server.conf })
        return render_to_response('hardware/server_edit.html', RequestContext(request,{'serverform':serverform}))
    else:
        serverform = ServerForm(request.POST)
        if serverform.is_valid():
            server = Server.objects.get(id=id)
            server.number = serverform.cleaned_data['number']
            server.manager = serverform.cleaned_data['manager']
            server.company = serverform.cleaned_data['company']
            server.product = serverform.cleaned_data['product']
            server.rack = serverform.cleaned_data['rack']
            server.conf = serverform.cleaned_data['conf']
            server.save()
            return render_to_response('hardware/server_edit.html', RequestContext(request,{'serverform':serverform}))
        else:
            return render_to_response('hardware/server_edit.html', RequestContext(request,{'serverform':serverform}))

@login_required
def server_delete(request, id):
    server = Server.objects.get(id=id)
    server.delete()
    return render_to_response('hardware/server_delete.html', RequestContext(request))

