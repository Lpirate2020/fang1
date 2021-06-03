from django.contrib import admin

# Register your models here.
from . import models


class HouseInfoAdmin(admin.ModelAdmin):  # 不显示id，图片存储地址
    list_display = (
        'name', 'house_state', 'price', 'price_m', 'choices', 'floor', 'area', 'structure', 'inside_area',
        'building_type',
        'orientation',
        'building_structure', 'decoration', 'proportion', 'lift', 'listing_time', 'transaction_type',
        'purpose',
        'ascription_year', 'property_right', 'mortgage', 'premises_permit', 'agent_name', 'region'
    )


# , 'last_time'

admin.site.site_url = "/admin"
admin.site.site_header = '房天下后台管理系统'
admin.site.site_title = '房天下后台管理系统'
admin.site.index_title = '欢迎使用房天下后台管理系统'

admin.site.register(models.HouseInfo, HouseInfoAdmin)
