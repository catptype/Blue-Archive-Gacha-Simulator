from django.contrib import admin
from django.utils.html import format_html
from django.template.loader import render_to_string

from .models import GachaBanner, GachaTransaction, GachaType
from .forms import GachaBannerAdminForm, GachaTransactionAdminForm, GachaTypeAdminForm

class GachaTypeAdmin(admin.ModelAdmin):
    form = GachaTypeAdminForm
    list_display = ['name', 'feature_rate', 'r3_rate', 'r2_rate', 'r1_rate']

    class Media:
        css = {
            'all': ('/static/css/admin-overrides.css',),
        }

class GachaTransactionAdmin(admin.ModelAdmin):
    form = GachaTransactionAdminForm
    list_display = ['user', 'banner','student', 'custom_datetime']
    list_per_page = 20

    def custom_datetime(self, obj):
        return obj.datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    custom_datetime.short_description = 'Datetime'

class GachaBannerAdmin(admin.ModelAdmin):
    form = GachaBannerAdminForm
    list_display = ['name', 'rates', 'is_pickup_portrait','not_pickup_portrait']
    list_per_page = 1
    filter_horizontal = ('is_pickup', 'not_pickup')

    def rates(self, obj):
        return format_html(
            f'<p>feature: {obj.feature_rate}%</p>'
            f'<p>★★★: {obj.r3_rate}%</p>'
            f'<p>★★: {obj.r2_rate}%</p>'
            f'<p>★: {obj.r1_rate}%</p>'
        )        

    def is_pickup_portrait(self, obj):
        students = obj.is_pickup.all().order_by('name')
        context = {
            'students': students,
            'rarities': [3],
        }
        return render_to_string('admin/gacha_banner.html', context)
    
    def not_pickup_portrait(self, obj):
        students = obj.not_pickup.all().order_by('name')
        context = {
            'students': students,
            'rarities': [3,2,1],
        }
        return render_to_string('admin/gacha_banner.html', context)

    is_pickup_portrait.short_description = 'Pickup 3★ students'
    not_pickup_portrait.short_description = 'Not pickup students'
    
    class Media:
        css = {
            'all': ('/static/css/admin-overrides.css',),
        }
        js = ('/static/js/admin.js',)

admin.site.register(GachaType, GachaTypeAdmin)
admin.site.register(GachaBanner, GachaBannerAdmin)
admin.site.register(GachaTransaction, GachaTransactionAdmin)