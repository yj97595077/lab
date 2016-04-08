# -*- coding: utf-8 -*-

from django import forms
from hardware.models import Rack
#from django.contrib.auth.models import User

class SignupForm(forms.Form):
    username = forms.CharField(
        label=u"用户名",
        required=True,
        error_messages={'required': '请输入用户名'},
        #help_text=u"请填写用户名",
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
        #help_text=u"请填写密码",
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
        #help_text=u"请再次填写密码",
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
        #help_text=u"请填写邮箱",
        widget=forms.EmailInput(
            attrs={
                'placeholder':u"邮箱",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名，密码和邮箱为必填项")
        else:
            cleaned_data = super(SignupForm, self).clean()
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        label=u"用户名",
        required=True,
        error_messages={'required': '请输入用户名'},
        #help_text=u"请填写用户名",
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
        #help_text=u"请填写密码",
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()
        return cleaned_data

class ServerForm(forms.Form):
    number = forms.CharField(
        label=u"资产编号",
        required=True,
        error_messages={'required': u'必选项'},
        #help_text=u"请填写资产编号",
    )
    manager = forms.CharField(
        label = u"负责人",
        required=True,
        error_messages={'required': u'必选项'},
        #help_text=u"请填写负责人",
    )
    company = forms.CharField(
        label = u"生产公司",
        required=True,
        error_messages={'required': u'必选项'},
        #help_text=u"请填写生产公司",
    )
    product = forms.CharField(
        label = u"生产型号",
        required=True,
        error_messages={'required': u'必选项'},
        #help_text=u"请填写生产型号",
    )
    rack = forms.ModelChoiceField(
        queryset=Rack.objects.all(),
        label=u"机架位置",
        required=True,
        error_messages={'required': u'必选项'},
        #help_text=u"请下拉菜单选择",
    )
    conf = forms.CharField(
        label=u"机器配置",
        required=True,
        error_messages={'required': u'必选项'},
        #help_text=u"请填写机器配置",
        widget=forms.Textarea(
            attrs={
                'placeholder':"在此填写机器的详细配置，例如CPU/内存/硬盘/网卡等",
                'rows':2,
                'style':"width:100%",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"以下红色标记部分为必选项")
        else:
            cleaned_data = super(ServerForm, self).clean()
        return cleaned_data
