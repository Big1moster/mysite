from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    #定制表单
    username = forms.CharField(label="用户名",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))  #默认label就是字段名username，默认required=True，不需要时可以手动设置
    #widget设置input的type属性值为password  ,添加一些bootstrap的类，做样式
    password = forms.CharField(label="密码",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        #用户验证可以不用request参数，login方法必须要
        user = auth.authenticate(username=username,password=password)
        if user is  None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            #将验证后的用户返回，到views中登录
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label="用户名"
                               ,max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入3-30位的用户名'}))

    email= forms.CharField(label="邮箱",
                           widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'请输入邮箱'}))

    password = forms.CharField(label="密码",
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    password_again = forms.CharField(label="再输入密码",
                                     min_length=6,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再次输入密码'}))
#加下划线 专门正对字段进行验证
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('密码不一致')
        return password_again

