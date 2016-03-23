# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class Rack(models.Model):
    name = models.CharField('机柜名称', max_length=256)
    manager = models.CharField('负责人', max_length=256)

    def __unicode__(self):
        return self.name

class Server(models.Model):
    number = models.CharField('资产编号', max_length=256)
    manager = models.CharField('负责人', max_length=256)
    company = models.CharField('生产厂商', max_length=256)
    product = models.CharField('生产型号', max_length=256)
    rack = models.ForeignKey(Rack, verbose_name='机架位置')
    conf = models.TextField('机器配置', max_length=256)

    def __unicode__(self):
        return self.number
