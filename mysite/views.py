from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from read_account.utils import get_seven_days_read_date,get_today_hot_data,get_yesterday_hot_data,get_seven_days_hot_blog
from blog.models import Blog
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User
from django.http import JsonResponse
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums ,dates= get_seven_days_read_date(blog_content_type)

    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

    # 获取7天热门博客的缓存数据，字典类型
    hot_blogs_for_seven_days = cache.get('hot_blogs_for_seven_days')
    #如果缓存表中无该数据
    if hot_blogs_for_seven_days is None:
        hot_blogs_for_seven_days = get_seven_days_hot_blog()
        #将该数据以键值加到缓存表中,并设置缓存时间/s
        cache.set('hot_blogs_for_seven_days',hot_blogs_for_seven_days,3600)
        print("计算")
    else:
        print("使用缓存")
    context={}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['hot_blogs_for_seven_days'] = hot_blogs_for_seven_days
    return render(request,'home.html',context)

def login(request):
    # username = request.POST.get('username','')  #取出POST类似字典中的username数据，若没有就默认空字符串
    # password = request.POST.get('password','')
    # user = auth.authenticate(request,username=username,password=password) #验证用户，如果没问题，返回真实user，否则返回none
    # #得到发送请求的网址，没有解析出别名为home的网址
    # referer = request.META.get("HTTP_REFERER",reverse('home'))
    # if user is not None:
    #     #如果验证通过，则登录用户
    #     auth.login(request,user)
    #     return redirect(referer)
    # else:
    #     return render(request,'error.html',{'message':"用户名或密码不正确"})

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from', reverse('home')))
            #以下注释内容都在forms.py中进行处理
            #经过验证后的数据（填写符合规范），字典
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
            # user = auth.authenticate(request,username=username,password = password)
            # if user is not None:
            #     auth.login(request,user)
            #     #跳转到点击登录的那个页面，否则回到首页
            #     return redirect(request.GET.get('from',reverse('home')))
            # else:
            #     login_form.add_error(None,'用户名或密码不正确')
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
       data['status'] = 'ERROR'
    return JsonResponse(data)
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        #数据是有效的即经过了验证
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username,email,password)
            user.save()

            user = auth.authenticate(username=username,password=password)  #验证用户
            # 登录用户,必须要request参数
            auth.login(request,user)
            # 跳转到点击注册的那个页面
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request,'register.html',context)

def logout(request):
    # 自带的登出功能
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request,'user_info.html',context)
