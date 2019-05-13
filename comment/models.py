from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)  # do_nothing删除不会影响到关联的数据表  关联对应模型
    object_id = models.PositiveIntegerField()  # 对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')  #评论的对象，具体博客
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    #多个字段关联同一外键就要设置related_name，通过related_name可以得到user关联的comment对象   user.comments.all()
    user = models.ForeignKey(User,related_name="comments",on_delete=models.DO_NOTHING)

    #回复功能新加字段
    #顶级评论
    root = models.ForeignKey('self',related_name="root_comment",null=True,on_delete=models.DO_NOTHING)
    #数据库的自关联
    parent = models.ForeignKey('self',related_name="parent_comment",null=True,on_delete=models.DO_NOTHING)
    # 回复谁，#通过related_name可以得到related_name关联的comment对象
    reply_to = models.ForeignKey(User,null=True,related_name="replies",on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.text
    class Meta:
        ordering = ['comment_time']
