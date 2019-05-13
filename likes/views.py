from django.shortcuts import render
from .models import LikeCount,LikeRecord
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
# Create your views here.
def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)
def ErrorResponse(code,message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)
def like_change(request):
    # 获取前端的数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400,'你没有登录')
    #str
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    #得到content_type对象
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,'对象不纯正')

    #处理数据
    if request.GET.get('is_like') == 'true':
        #要点赞
        like_record,created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        if created:
            #未点赞过，进行点赞
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            return ErrorResponse(401,'重复点赞')

    else:
        #取消点赞
        if LikeRecord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
            #有点赞过，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            like_count = LikeCount.objects.get(content_type=content_type, object_id=object_id)
            like_count.liked_num -= 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            return ErrorResponse(403,'你没有点赞过')
