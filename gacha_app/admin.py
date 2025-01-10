from django.contrib import admin
from django.utils.html import format_html
from django.template.loader import render_to_string

from .models import GachaBanner, GachaTransaction, GachaRatePreset
from .forms import GachaBannerAdminForm, GachaTransactionAdminForm, GachaRatePresetAdminForm

class GachaRatePresetAdmin(admin.ModelAdmin):
    form = GachaRatePresetAdminForm
    list_display = ['preset_id','preset_name', 'preset_feature_rate', 'preset_r3_rate', 'preset_r2_rate', 'preset_r1_rate']

    class Media:
        css = {
            'all': ('/static/css/admin-overrides.css',),
        }

class GachaTransactionAdmin(admin.ModelAdmin):
    form = GachaTransactionAdminForm
    list_display = ['transaction_id', 'user', 'banner', 'student', 'datetime']
    list_per_page = 20

    @admin.display(description='User')
    def user(self, obj:GachaTransaction) -> str:
        return obj.user

    @admin.display(description='Banner')
    def banner(self, obj:GachaTransaction) -> str:
        return obj.banner_name

    @admin.display(description='Student')
    def student(self, obj:GachaTransaction) -> str:
        return obj.student
    
    @admin.display(description='Datetime')
    def datetime(self, obj:GachaTransaction) -> str:
        return obj.datetime

class GachaBannerAdmin(admin.ModelAdmin):
    form = GachaBannerAdminForm
    list_display = ['banner_name', 'rates', 'is_pickup_portrait','not_pickup_portrait']
    list_per_page = 1
    filter_horizontal = ('banner_pickup', 'banner_non_pickup')

    def rates(self, obj:GachaBanner):
        return format_html(
            f'<p>feature: {obj.preset_id.feature}%</p>'
            f'<p>★★★: {obj.preset_id.r3}%</p>'
            f'<p>★★: {obj.preset_id.r2}%</p>'
            f'<p>★: {obj.preset_id.r1}%</p>'
        )        

    @admin.display(description='Pickup 3★ students')
    def is_pickup_portrait(self, obj:GachaBanner):
        students = obj.banner_pickup.order_by('student_name')
        context = {
            'students': students,
            'rarities': [3],
        }
        return render_to_string('admin/gacha_banner.html', context)
    
    @admin.display(description='Not pickup students')
    def not_pickup_portrait(self, obj:GachaBanner):
        students = obj.banner_non_pickup.order_by('student_name')
        context = {
            'students': students,
            'rarities': [3,2,1],
        }
        return render_to_string('admin/gacha_banner.html', context)
    
    class Media:
        css = {
            'all': ('/static/css/admin-overrides.css',),
        }
        js = ('/static/js/admin.js',)

admin.site.register(GachaRatePreset, GachaRatePresetAdmin)
admin.site.register(GachaBanner, GachaBannerAdmin)
admin.site.register(GachaTransaction, GachaTransactionAdmin)