# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from hardware.models import *

class SignupForm(forms.Form):
    username = forms.CharField(
        label=u"用户名",
        required=True,
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名",
            }
        ),
    )
    password = forms.CharField(
        label=u"密码",
        required=True,
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
            }
        ),
    )
    repeat_password = forms.CharField(
        label=u"重复密码",
        required=True,
        error_messages={'required': u'请再次输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"重复密码",
            }
        ),
    )
    email = forms.EmailField(
        label=u"邮箱",
        required=True,
        error_messages={'required': u'请输入邮箱'},
        widget=forms.EmailInput(
            attrs={
                'placeholder':u"邮箱",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"以下红色标记部分为必选项")
        else:
            cleaned_data = super(SignupForm, self).clean()
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        label=u"用户名",
        required=True,
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名",
            }
        ),
    )
    password = forms.CharField(
        label=u"密码",
        required=True,
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"以下红色标记部分为必选项")
        else:
            cleaned_data = super(LoginForm, self).clean()
        return cleaned_data

class ServerForm(ModelForm):
    class Meta:
        model = Server
        fields = (
            'number',
            'manager',
            'company',
            'product',
            'rack',
            'conf',
            'state',
            'system',
            'version',
            'service',
            'hostname',
            'ipmi_ip',
            'ipmi_user',
            'ipmi_passwd',
            'sys_ip',
            'sys_user',
            'sys_passwd',
        )

class SwitchForm(ModelForm):
    class Meta:
        model = Switch
        fields = (
            'number',
            'manager',
            'company',
            'product',
            'rack',
            'state',
            'service',
            'hostname',
            'sys_ip',
            'sys_user',
            'sys_passwd',
        )

class IPForm(ModelForm):
    ip_start = forms.CharField(
        label=u"起始IP",
        required=True,
        error_messages={'required': u'请输入起始IP'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"起始IP",
            }
        ),
    )
    ip_end = forms.CharField(
        label=u"终止IP",
        required=True,
        error_messages={'required': u'请输入终止IP'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"终止IP",
            }
        ),
    )
    class Meta:
        model = IP
        fields = (
            #'ip',
            'ip_start',
            'ip_end',
            'network',
            'manager',
            'project',
            'rack',
            'service',
            'time_start',
            'time_end',
            'notes',
        )
        widgets={
            'time_start': forms.TextInput(attrs={'placeholder': u'时间格式：xxxx-xx-xx，例如2016-01-01'}),
            'time_end': forms.TextInput(attrs={'placeholder': u'时间格式：xxxx-xx-xx，例如2016-01-01'}),
        }

