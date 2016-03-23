# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name=b'\xe6\x9c\xba\xe6\x9f\x9c\xe5\x90\x8d\xe7\xa7\xb0')),
                ('manager', models.CharField(max_length=256, verbose_name=b'\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba')),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField(max_length=256, verbose_name=b'\xe8\xb5\x84\xe4\xba\xa7\xe7\xbc\x96\xe5\x8f\xb7')),
                ('manager', models.CharField(max_length=256, verbose_name=b'\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba')),
                ('company', models.CharField(max_length=256, verbose_name=b'\xe7\x94\x9f\xe4\xba\xa7\xe5\x8e\x82\xe5\x95\x86')),
                ('product', models.CharField(max_length=256, verbose_name=b'\xe7\x94\x9f\xe4\xba\xa7\xe5\x9e\x8b\xe5\x8f\xb7')),
                ('conf', models.TextField(max_length=256, verbose_name=b'\xe6\x9c\xba\xe5\x99\xa8\xe9\x85\x8d\xe7\xbd\xae')),
                ('rack', models.ForeignKey(verbose_name=b'\xe6\x9c\xba\xe6\x9e\xb6\xe4\xbd\x8d\xe7\xbd\xae', to='hardware.Rack')),
            ],
        ),
    ]
