# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Manager(models.Model):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    name = models.CharField('姓名', max_length = 256)
    gender = models.CharField('性别', max_length = 256, choices = GENDER_CHOICES)
    email = models.EmailField('邮箱')
    phone = models.CharField('电话', max_length = 256)

    def __unicode__(self):
        return self.name

class Company(models.Model):
    name = models.CharField('公司名称', max_length = 256)
    contact = models.CharField('公司联系人', max_length = 256)
    email = models.EmailField('联系人邮箱')
    phone = models.CharField('联系人电话', max_length = 256)

    def __unicode__(self):
        return self.name

class Rack(models.Model):
    name = models.CharField('机柜名称', max_length = 256)
    manager = models.ManyToManyField(Manager, verbose_name = '负责人')
    description = models.TextField('机柜描述', max_length = 256)

    def __unicode__(self):
        return self.name

class Server(models.Model):
    SYSTEM_CHOICES = (
        ('Windows', 'Windows'),
        ('Redhat', 'Redhat'),
        ('CentOS', 'CentOS'),
        ('Debian', 'Debian'),
        ('Ubuntu', 'Ubuntu'),
        ('Others', '其它'),
        ('NotDeployed', '未部署'),
    )
    number = models.CharField('资产编号', max_length = 256)
    manager = models.ManyToManyField(Manager, verbose_name = '负责人')
    company = models.ForeignKey(Company, verbose_name = '生产厂商')
    product = models.CharField('生产型号', max_length = 256)
    time = models.DateTimeField('进场时间', auto_now_add = True)
    rack = models.ForeignKey(Rack, verbose_name = '机柜')
    conf = models.TextField('机器配置', max_length = 256)
    state = models.CharField('状态', max_length = 256, choices = (('enable', '可用'),('disable', '不可用'),))
    system = models.CharField('操作系统', max_length = 256, choices = SYSTEM_CHOICES)
    version = models.CharField('系统版本', max_length = 256, blank = True)
    service = models.CharField('业务', max_length = 256, blank = True)
    hostname = models.CharField('主机名', max_length = 256, blank = True)
    ipmi_ip = models.CharField('IPMI的IP', max_length = 256, blank = True)
    ipmi_user = models.CharField('IPMI的用户名', max_length = 256, blank = True)
    ipmi_passwd = models.CharField('IPMI的密码', max_length = 256, blank = True)
    sys_ip = models.CharField('系统的IP', max_length = 256, blank = True)
    sys_user = models.CharField('系统的用户名', max_length = 256, blank = True)
    sys_passwd = models.CharField('系统的密码', max_length = 256, blank = True)

    def __unicode__(self):
        return self.number

