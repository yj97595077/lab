# -*- coding: utf-8 -*-
from easysnmp import Session
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
    if arg == {}:
        servers = Server.objects.all()
    else:
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
    servers = servers.extra(select={'number_int': 'number+0'}).extra(order_by=['number_int'])
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
def switch(request, **arg):
    managers = Manager.objects.all()
    companys = Company.objects.all()
    racks = Rack.objects.all()
    state_list = ['enable', 'disable']
    if arg == {}:
        switches = Switch.objects.all()
    else:
        for x in arg:
            if x == "search":
                search = arg[x]
            if x == "id":
                id = arg[x]
            if x == "item":
                item = arg[x]
        if search == "manager":
            manager = Manager.objects.get(id = id)
            switches = Switch.objects.filter(manager = manager)
        if search == "company":
            company = Company.objects.get(id = id)
            switches = Switch.objects.filter(company = company)
        if search == "rack":
            rack = Rack.objects.get(id = id)
            switches = Switch.objects.filter(rack = rack)
        if search == "state":
            state = item
            switches = Switch.objects.filter(state = state)
    switches = switches.extra(select={'number_int': 'number+0'}).extra(order_by=['number_int'])
    paginator = Paginator(switches, 5) # 实例化一个分页对象
    page = request.GET.get('page') # 获取页码
    try:
        switches = paginator.page(page) # 获取某页对应的记录
    except PageNotAnInteger: # 如果页码不是个整数
        switches = paginator.page(1) # 取第一页的记录
    except (InvalidPage, EmptyPage): # 如果页码太大，没有相应的记录
        switches = paginator.page(paginator.num_pages) # 取最后一页的记录
    content = {
        'managers': managers,
        'companys': companys,
        'racks': racks,
        'state_list': state_list,
        'switches': switches,
    }
    return render_to_response('hardware/switch.html', RequestContext(request, content))

@login_required
def switch_add(request):
    if request.method == 'GET':
        switchform = SwitchForm()
    else:
        switchform = SwitchForm(request.POST)
        if switchform.is_valid():
            switch = switchform.save()
            switch.save()
            return render_to_response('hardware/jump.html', RequestContext(request, {'switch_add_success': True}))
    return render_to_response('hardware/switch_add.html', RequestContext(request, {'switchform': switchform}))

@login_required
def switch_edit(request, id):
    if request.method == 'GET':
        switch = Switch.objects.get(id=id)
        switchform = SwitchForm(instance = switch)
    else:
        switch = Switch.objects.get(id=id)
        switchform = SwitchForm(request.POST, instance = switch)
        if switchform.is_valid():
            switchform.save()
            return render_to_response('hardware/jump.html', RequestContext(request, {'switch_edit_success': True}))
    return render_to_response('hardware/switch_edit.html', RequestContext(request, {'switchform': switchform}))

@login_required
def switch_delete(request, id):
    switch = Switch.objects.get(id=id)
    switch.delete()
    return render_to_response('hardware/jump.html', RequestContext(request, {'switch_delete_success': True}))

@login_required
def switch_detail(request, id):
    switches = Switch.objects.filter(id=id)
    #switches = Switch.objects.filter(state="enable") #测试竖向表格展示
    return render_to_response('hardware/switch_detail.html', RequestContext(request, {'switches': switches}))

@login_required
def switch_telnet(request, id):
    url = "192.168.112.110"
    return render_to_response('hardware/switch_telnet.html', RequestContext(request, {'url': '10.2.41.182:443'}))

@login_required
def switch_manage(request, id):
    switch = Switch.objects.get(id = id)
    switch_snmp = Session(hostname=switch.sys_ip, community='public', version=2)
    cpu_info = switch_snmp.get(".1.3.6.1.4.1.4413.1.1.1.1.4.9.0")
    cpu = cpu_info.value[(cpu_info.value.find('(')+2):(cpu_info.value.find(')')-1)]
    cpu = float(cpu)
    #system_info = switch_snmp.get_bulk(".1.3.6.1.4.1.4413.1.1.1.1.4.9",0,10)
    #system_info = switch_snmp.walk(".1.3.6.1.2.1.2.2.1.2")
    return render_to_response('hardware/switch_manage.html', RequestContext(request, {'cpu': cpu}))

@login_required
# 由于传递的变量数目可能少于所有列出的，所以必须得用可变参数传递。
# arg = {'search':'network/manager/xxx', 'id':'xxx', 'item':'xxx'}
def ip(request, **arg):
    networks = Network.objects.all()
    managers = Manager.objects.all()
    racks = Rack.objects.all()
    if arg == {}:
        ips = IP.objects.all()
    else:
        for x in arg:
            if x == "search":
                search = arg[x]
            if x == "id":
                id = arg[x]
        if search == "network":
            network = Network.objects.get(id = id)
            ips = IP.objects.filter(network = network)
        if search == "manager":
            manager = Manager.objects.get(id = id)
            ips = IP.objects.filter(manager = manager)
        if search == "rack":
            rack = Rack.objects.get(id = id)
            ips = IP.objects.filter(rack = rack)
    ips = ips.extra(select={'ipa': "inet_aton(ip)"}).extra(order_by=['ipa'])
    paginator = Paginator(ips, 10) # 实例化一个分页对象
    page = request.GET.get('page') # 获取页码
    try:
        ips = paginator.page(page) # 获取某页对应的记录
    except PageNotAnInteger: # 如果页码不是个整数
        ips = paginator.page(1) # 取第一页的记录
    except (InvalidPage, EmptyPage): # 如果页码太大，没有相应的记录
        ips = paginator.page(paginator.num_pages) # 取最后一页的记录
    content = {
        'networks': networks,
        'managers': managers,
        'racks': racks,
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

@login_required
def ip_delete(request, id=None):
    print request.POST
    if id != None:
        ip = IP.objects.get(id=id)
        ip.delete()
    else:
        ip_id_list = request.POST.getlist('ip_id')
        print "hello1"
        print ip_id_list
        for ip_id in ip_id_list:
            print "hello2"
            print ip_id
            #ip = IP.objects.get(id=int(ip_id))
            #ip.delete()
    return render_to_response('hardware/jump.html', RequestContext(request, {'ip_delete_success': True}))

