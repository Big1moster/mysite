from django import template
from ..models import Comment
from django.contrib.contenttypes.models import ContentType
#注册我们自定义的标签，只有注册过的标签，系统才能认识你，这是固定写法
register = template.Library()
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)

    return Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()


