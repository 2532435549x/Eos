from django.contrib import admin

# Register your models here.
from Query_system.models import *

admin.site.register(token_action) #注册数据库到admin数据库管理，参数是models.py里操作数据库表的类