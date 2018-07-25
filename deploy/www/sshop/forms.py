from django import forms

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mail = forms.CharField(label='邮箱', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}))
    password = forms.CharField(label='密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    password_confirm = forms.CharField(label='确认密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    invite_user = forms.CharField(label='推荐人', max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ChangeForm(forms.Form):
    old_password = forms.CharField(label='原密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    password = forms.CharField(label='新密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    password_confirm = forms.CharField(label='确认密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))


class ResetForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mail = forms.CharField(label='注册邮箱', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}))
    password = forms.CharField(label='新密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    password_confirm = forms.CharField(label='确认密码', max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
