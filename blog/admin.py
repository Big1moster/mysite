from django.contrib import admin
from .models import BlogType,Blog
# Register your models here.


#若要把app应用显示在后台管理中，需要在admin.py中注册。这个注册有两种方式

@admin.register(BlogType)  #111装饰器注册
#BlogType模型管理器：
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')#在管理界面的显示列表,字段或方法
    

#admin.site.register(BlogType,BlogTypeAdmin)#222在admin中注册绑定

@admin.register(Blog)
#Blog模型管理器：
class BlogAdmin(admin.ModelAdmin):
    list_display=('id','title','blog_type','author','get_read_num','create_time','last_updated_time')
