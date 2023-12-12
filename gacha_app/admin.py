from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Student, School
from .forms import StudentAdminForm

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_student_names']

    def get_student_names(self, obj):
        return obj.get_student_names()

    get_student_names.short_description = 'members'  # Optional:

class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ['image_tag', 'name', 'version', 'rarity', 'school', 'is_limited', 'edit_button']
    
    def image_tag(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="width: auto; height:80px" />')
        return 'No Image'

    def edit_button(self, obj):
        change_url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name),  args=[obj.id])
        return format_html(f'<a href="{change_url}" class="button" style="font-weight: bold; text-decoration: none; padding: 5px 10px">EDIT</a>')
    
    image_tag.short_description = 'Image'
    edit_button.short_description = ''

    class Media:
        css = {
            'all': ('admin_styles.css',),
        }

admin.site.register(Student, StudentAdmin)
admin.site.register(School, SchoolAdmin)
