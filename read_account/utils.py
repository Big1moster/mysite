import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail
from django.utils import timezone
from django.db.models import Sum
from blog.models import Blog


def read_account_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        #总阅读数加一
        readnum,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     # 存在记录
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # # 计数加一
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数加一
        date = timezone.now().date()
        readDetail,created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk,date=date).count():
        #     # 存在记录
        #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj,date=date)
        # else:
        #     readDetail = ReadDetail(content_type=ct, object_id=obj.pk,date=date)
        # 计数加一
        readDetail.read_num += 1
        readDetail.save()
    return key

#得到前7天不包括今天的每天阅读数
def get_seven_days_read_date(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in  range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m%d')) #把时间对象变为时间字符串
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        #每天的阅读数量
        result = read_details.aggregate(read_num_sum =Sum('read_num')) #返回字典，{ 'read_num_sum':sum}
        read_nums.append(result['read_num_sum'] or 0)  #如果阅读数为nono则显示0
    return read_nums,dates

def get_today_hot_data(content_type):
    today = timezone.now().date()
    # 将今天被阅读的博客按照阅读数量倒序排列
    read_details = ReadDetail.objects.filter(content_type=content_type,date = today).order_by('-read_num')
    return read_details[0:7]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today-datetime.timedelta(days=1)
    # 将昨天被阅读的博客按照阅读数量倒序排列
    read_details = ReadDetail.objects.filter(content_type=content_type,date = today).order_by('-read_num')
    return read_details[0:7]

def get_seven_days_hot_blog():
    today = timezone.now().date()

    date = today -datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lte=today,read_details__date__gte=date)\
        .values('id','title')\
        .annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    #values按指定字段进行分组，annotate进行求和
    # read_details = ReadDetail.objects.filter(content_type=content_type,date__lt=today,date__gte=date)\
    #     .values('content_type','object_id')\
    #     .annotate(read_num_sum=Sum('read_num'))\
    #     .order_by('-read_num_sum')
    return blogs[:7]