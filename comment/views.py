from django.shortcuts import render,redirect
from .models import Comment
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.

def update_comment(request):

    # referer = request.META.get("HTTP_REFERER", reverse('home'))
    # user = request.user
    # if user.is_authenticated:
    #     return render(request, 'error.html', {'message': "用户名未登录"})
    # text = request.POST.get('text','').strip()
    # if text == '':
    #     return render(request, 'error.html', {'message': "评论内容为空"})
    # try:
    #     content_type = request.POST.get('content_type','')
    #     object_id = int(request.POST.get('object_id',''))
    #     #得到Blog类
    #     model_class = ContentType.objects.get(model=content_type).model_class()
    #     #得到评论的具体那篇博客对象
    #     model_obj = model_class.objects.get(pk=object_id)
    # except:
    #     return render(request, 'error.html', {'message': "评论对象不存在",'redirect_to':referer})
    # #数据正常后创建评论对象
    # comment = Comment()
    # comment.user = user
    # comment.text = text
    # comment.content_object = model_obj
    # comment.save()
    # # 得到发送请求的网址，没有则解析出别名为home的网址
    #
    # return redirect(referer)
    referer = request.META.get("HTTP_REFERER", reverse('home'))
    #初始化的时候让CommentForm接收user这个参数，验证用户是否登录
    comment_form = CommentForm(request.POST,user=request.user)
    data = {}
    if comment_form.is_valid():
        #检查通过
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        # 如果不是评论而是回复
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        #返回数据
        data['status'] = "SUCCESS"
        data['username'] = comment.user.username
        # 将时间对象转换为字符串格式
        data['comment_time']=comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text']= comment.text
        #得到对应的字符串
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        # return redirect(referer)
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
    else:
        data['status'] = 'ERROR'
        # 返回错误信息中的一个
        data['message']=list(comment_form.errors.values())[0][0]
        #comment_form.errors即raise forms.ValidationError('评论对象不存在')的信息
       # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
    return JsonResponse(data)


