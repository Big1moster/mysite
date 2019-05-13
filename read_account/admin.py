from django.contrib import admin
from .models import ReadNum,ReadDetail

# Register your models here.

@admin.register(ReadNum)
#Blog模型管理器：
class ReadNumAdmin(admin.ModelAdmin):
    list_display=('read_num','content_object')

@admin.register(ReadDetail)
#Blog模型管理器：
class ReadDetailAdmin(admin.ModelAdmin):
    list_display=('date','read_num','content_object')