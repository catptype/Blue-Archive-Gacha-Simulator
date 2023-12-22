from django.contrib import admin
from django.utils.html import format_html

from student_app.models import Student

from .models import GachaBanner, GachaTransaction
from .forms import GachaBannerAdminForm, GachaTransactionAdminForm

class GachaTransactionAdmin(admin.ModelAdmin):
    form = GachaTransactionAdminForm
    list_display = ['user', 'banner','student', 'datetime']
    list_per_page = 20

class GachaBannerAdmin(admin.ModelAdmin):
    form = GachaBannerAdminForm
    list_display = ['name', 'is_pickup_img','not_pickup_img']
    list_per_page = 1
    filter_horizontal = ('is_pickup', 'not_pickup')

    def get_student_images_html(self, students, rarity_symbol):

        images_html = [
            f'<div class="student-item">'
            f'<img src="{student.image.url}" alt="{student.name}_{student.version}" style="height:80px;">'
            f'<figcaption>{student.name}{("_" + student.version.name if student.version.name != "Original" else "")}</figcaption>'
            f'</div>'
            for student in students
        ]
        
        html = [
            f'<div><h3>{rarity_symbol}</h3>'
            f'<div class="student-grid">'
            f'{''.join(images_html)}'
            f'</div>'
            f'</div>'
        ]
        return ''.join(html)

    def render_student_images(self, students):
        images_html = []

        for i, student_query in enumerate(students):
            if student_query:
                images_html.extend(self.get_student_images_html(student_query, '★' * (3-i)))

        return format_html(''.join(images_html))

    def not_pickup_img(self, obj):
        return self.render_student_images(
            [obj.not_pickup.filter(rarity=r).order_by('name') for r in [3, 2, 1]],
        )

    def is_pickup_img(self, obj):
        return self.render_student_images(
            [obj.is_pickup.filter(rarity=r).order_by('name') for r in [3, 2, 1]],
        )
    
    is_pickup_img.short_description = 'Pickup 3★ students'
    not_pickup_img.short_description = 'Available students'
    
    class Media:
        css = {
            'all': ('/static/css/admin_banner.css',),
        } 

admin.site.register(GachaBanner, GachaBannerAdmin)
admin.site.register(GachaTransaction, GachaTransactionAdmin)