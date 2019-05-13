from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

# Create your models here.
class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # do_nothing删除不会影响到关联的数据表  关联对应模型
    object_id = models.PositiveIntegerField() #对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面2个字段统一起来变成通用外键


class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    date = models.DateTimeField(default=timezone.now)
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # do_nothing删除不会影响到关联的数据表  关联对应模型
    object_id = models.PositiveIntegerField() #对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')  # 将上面2个字段统一起来变成通用外键
