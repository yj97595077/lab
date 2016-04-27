# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from hardware.models import *
from hardware.forms import *

# Create your views here.

def home(request):
    return render_to_response('hardware/home.html', RequestContext(request))

def about(request):
    return render_to_response('hardware/about.html', RequestContext(request))

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    repeat_password_error = False
    user_exist_error = False
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
                return render_to_response('hardware/jump.html',RequestContext(request, {'signup_success': True}))
    content = {
        'signupform': signupform,
        'repeat_password_error': repeat_password_error,
        'user_exist_error': user_exist_error,
    }
    return render_to_response('hardware/signup.html',RequestContext(request, content))

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    password_wrong_error = False
    if request.method == 'GET':
        loginform = LoginForm()
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
                password_wrong_error = True
    return render_to_response('hardware/login.html', RequestContext(request, {'loginform': loginform, 'password_wrong_error': password_wrong_error}))

def logout(request):
    auth.logout(request)
    return render_to_response('hardware/jump.html', RequestContext(request, {'logout_success': True}))

@login_required
#由于传递的变量数目可能少于所有列出的，所以必须得用可变参数传递。
def server(request, **arg):
    managers = Manager.objects.all()
    companys = Company.objects.all()
    racks = Rack.objects.all()
    state_list = ['enable', 'disable']
    system_list = ['Windows', 'Redhat', 'CentOS', 'Debian', 'Ubuntu', 'Others', 'NotDeployed']
    if arg != {}:
        for x in arg:
            if x == "search":
                search = arg[x]
            if x == "id":
                id = arg[x]
            if x == "item":
                item = arg[x]
        if search == "manager":
            manager = Manager.objects.get(id = id)
            servers = Server.objects.filter(manager = manager)
        if search == "company":
            company = Company.objects.get(id = id)
            servers = Server.objects.filter(company = company)
        if search == "rack":
            rack = Rack.objects.get(id = id)
            servers = Server.objects.filter(rack = rack)
        if search == "state":
            state = item
            servers = Server.objects.filter(state = state)
        if search == "system":
            system = item
            servers = Server.objects.filter(system = system)
    else:
        servers = Server.objects.all()
    paginator = Paginator(servers, 5) # 实例化一个分页对象
    page = request.GET.get('page') # 获取页码
    try:
        servers = paginator.page(page) # 获取某页对应的记录
    except PageNotAnInteger: # 如果页码不是个整数
        servers = paginator.page(1) # 取第一页的记录
    except (InvalidPage, EmptyPage): # 如果页码太大，没有相应的记录
        servers = paginator.page(paginator.num_pages) # 取最后一页的记录
    content = {
        'managers': managers,
        'companys': companys,
        'racks': racks,
        'state_list': state_list,
        'system_list': system_list,
        'servers': servers,
    }
    return render_to_response('hardware/server.html', RequestContext(request, content))

@login_required
def server_add(request):
    if request.method == 'GET':
        serverform = ServerForm()
    else:
        serverform = ServerForm(request.POST)
        if serverform.is_valid():
            server = serverform.save()
            server.save()
            return render_to_response('hardware/jump.html', RequestContext(request, {'server_add_success': True}))
    return render_to_response('hardware/server_add.html', RequestContext(request, {'serverform': serverform}))

@login_required
def server_edit(request, id):
    if request.method == 'GET':
        server = Server.objects.get(id=id)
        serverform = ServerForm(instance = server)
    else:
        server = Server.objects.get(id=id)
        serverform = ServerForm(request.POST, instance = server)
        if serverform.is_valid():
            serverform.save()
            return render_to_response('hardware/jump.html', RequestContext(request, {'server_edit_success': True}))
    return render_to_response('hardware/server_edit.html', RequestContext(request, {'serverform': serverform}))

@login_required
def server_delete(request, id):
    server = Server.objects.get(id=id)
    server.delete()
    return render_to_response('hardware/jump.html', RequestContext(request, {'server_delete_success': True}))

@login_required
def server_detail(request, id):
    servers = Server.objects.filter(id=id)
    #servers = Server.objects.filter(state="enable") #测试竖向表格展示
    return render_to_response('hardware/server_detail.html', RequestContext(request, {'servers': servers}))

@login_required
def server_ssh(request, id):
    url = "192.168.112.110"
    return render_to_response('hardware/server_ssh.html', RequestContext(request, {'url': '10.2.41.182:443'}))

@login_required
#由于传递的变量数目可能少于所有列出的，所以必须得用可变参数传递。
def ip(request, **arg):
    managers = Manager.objects.all()
    racks = Rack.objects.all()
    state_list = ['enable', 'disable']
    if arg != {}:
        for x in arg:
            if x == "search":
                search = arg[x]
            if x == "id":
                id = arg[x]
            if x == "item":
                item = arg[x]
        if search == "manager":
            manager = Manager.objects.get(id = id)
            ips = IP.objects.filter(manager = manager)
        if search == "rack":
            rack = Rack.objects.get(id = id)
            ips = IP.objects.filter(rack = rack)
        if search == "state":
            state = item
            ips = IP.objects.filter(state = state)
    else:
        ips = IP.objects.all()
    paginator = Paginator(ips, 10) # 实例化一个分页对象
    page = request.GET.get('page') # 获取页码
    try:
        ips = paginator.page(page) # 获取某页对应的记录
    except PageNotAnInteger: # 如果页码不是个整数
        ips = paginator.page(1) # 取第一页的记录
    except (InvalidPage, EmptyPage): # 如果页码太大，没有相应的记录
        ips = paginator.page(paginator.num_pages) # 取最后一页的记录
    content = {
        'managers': managers,
        'racks': racks,
        'state_list': state_list,
        'ips': ips,
    }
    return render_to_response('hardware/ip.html', RequestContext(request, content))

@login_required
def ip_add(request):
    ip_segment_error = False
    ip_exist_error = False
    if request.method == 'GET':
        ipform = IPForm()
    else:
        ipform = IPForm(request.POST)
        if ipform.is_valid():
            # 从起止IP中得到一个IP列表
            ip_start = ipform.cleaned_data['ip_start']
            ip_end = ipform.cleaned_data['ip_end']
            ip_start_split = ip_start.split('.')
            ip_end_split = ip_end.split('.')
            if ip_start_split[0] == ip_end_split[0] and ip_start_split[1] == ip_end_split[1] and ip_start_split[2] == ip_end_split[2]:
                ip_segment_range = range(int(ip_start_split[3]), (int(ip_end_split[3]) + 1))
                for ip_segment in ip_segment_range:
                    ip = str(ip_start_split[0]) + '.' + str(ip_start_split[1]) + '.' + str(ip_start_split[2]) + '.' + str(ip_segment)
                    if IP.objects.filter(ip = ip).exists():
                        ip_exist_error = True
                        break
                if ip_exist_error == False:
                    ip = str(ip_start_split[0]) + '.' + str(ip_start_split[1]) + '.' + str(ip_start_split[2]) + '.' + str(ip_segment_range[0])
                    new_ip = ipform.save(commit = False)
                    new_ip.ip = ip
                    new_ip.save()
                    new_ip_id = new_ip.id
                    ipform.save_m2m()
                    if len(ip_segment_range) >= 2:
                        for ip_segment in ip_segment_range[1:]:
                            ip = str(ip_start_split[0]) + '.' + str(ip_start_split[1]) + '.' + str(ip_start_split[2]) + '.' + str(ip_segment)
                            new_ip = ipform.save(commit = False)
                            new_ip.ip = ip
                            new_ip.id = new_ip_id + 1
                            new_ip.save(force_insert = True)
                            new_ip_id = new_ip.id
                            ipform.save_m2m()
                    return render_to_response('hardware/jump.html', RequestContext(request, {'ip_add_success': True}))
            else:
                ip_segment_error = True
    content = {
        'ip_segment_error': ip_segment_error,
        'ip_exist_error': ip_exist_error,
        'ipform': ipform,
    }
    return render_to_response('hardware/ip_add.html', RequestContext(request, content))

