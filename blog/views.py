from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from read_account.utils import read_account_once_read
from comment.models import Comment
from comment.forms import CommentForm
from mysite.forms import LoginForm
# 公共数据
def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUM)  # 每4页进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数，默认为1
    page_of_blogs = paginator.get_page(page_num)  # 不在范围则返回默认值1
    current_page_num = page_of_blogs.number  # 获取当前页码,前后两页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # page_range = [(current_page_num+i) for i in range(-3,3) if paginator.num_pages>=(current_page_num+i)>0]
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    # 等价于BlogType.objects.annotate(blog_count=Count('blog'))#blog是BlogType相关联字段的小写    运行时加入内存，比下面一开始就加入内存好一点
    '''blog_types=BlogType.objects.all()
    blog_types_list=[]
    for blog_type in blog_types:
        blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)

        '''
    # 获取日期归档对应博客数量
    blog_dates_dict = {}
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year, create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))  # 使用annotate拓展查询字段
    context['blog_dates'] = blog_dates_dict
    return context


# Create your views here.
def blog_list(request):  # 博客列表
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


# 博客类型归档处理函数
def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


# 博客日期归档处理函数
def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)


# 博客具体文章处理函数
def blog_detail(request, blog_pk):  # 博客文章
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookies_key = read_account_once_read(request, blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    #得到该博客的一级评论数据，不包括回复
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog'] = blog
    context['login_form'] = LoginForm()
    context['comments'] = comments.order_by('-comment_time')
    # #得到评论数，传给前端页面
    # context['comment_count'] = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk).count()
    #初始化form中2个字段的值
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_pk,'replay_comment_id':0})
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(read_cookies_key,'true')  # 阅读cookies标记  设置有效期 1： max_age=60  以秒为单位  2： expires=datetime对象  具体时间，到了时间就失效
    return response
