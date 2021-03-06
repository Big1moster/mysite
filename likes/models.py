from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()  #
    content_object = GenericForeignKey('content_type', 'object_id')

    liked_num = models.IntegerField(default=0)

class LikeRecord(models.Model):

    #被点赞对象信息
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()  # 对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 点赞日期
    liked_time = models.DateTimeField(auto_now_add=True)

