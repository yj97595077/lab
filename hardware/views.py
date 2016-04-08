from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from hardware.models import Rack, Server
from hardware.forms import SignupForm, LoginForm, ServerForm

# Create your views here.

def home(request):
    return render_to_response('hardware/home.html', RequestContext(request))

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    repeat_password_error = False
    user_exist_error = False
    signup_success = False
    if request.method == 'GET':
        signupform = SignupForm()
    else:
        signupform = SignupForm(request.POST)
        if signupform.is_valid():
            username = signupform.cleaned_data['username']
            password = signupform.cleaned_data['password']
            repeat_password = signupform.cleaned_data['repeat_password']
            email = signupform.cleaned_data['email']
            if password != repeat_password:
                repeat_password_error = True
            if User.objects.filter(username = username):
                user_exist_error = True
            if not user_exist_error and not repeat_password_error:
                new_user = User()
                new_user.username = username
                new_user.password = password
                new_user.email = email
                new_user.set_password(password)#密码保存分两步，一步存数据，一步加密，少哪个都不行。
                new_user.save()
                signup_success = True
                #下面这两句是要注册成功后自动登录的。
                user = auth.authenticate(username = username, password = password)
                auth.login(request, user)
    content = {
        'signupform': signupform,
        'repeat_password_error': repeat_password_error,
        'user_exist_error': user_exist_error,
        'signup_success': signup_success,
    }
    return render_to_response('hardware/signup.html',RequestContext(request, content))

def login(request):
    if request.method == 'GET':
        loginform = LoginForm()
        return render_to_response('hardware/login.html', RequestContext(request, {'loginform': loginform,}))
    else:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.cleaned_data['username']
            password = loginform.cleaned_data['password']
            user = auth.authenticate(username = username, password = password)
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

