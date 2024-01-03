from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.template.loader import render_to_string

from .models import Student, School, Version
from .forms import StudentAdminForm

class RarityFilter(admin.SimpleListFilter):
    title = "rarity"
    parameter_name = "rarity"

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        rarity_values = queryset.order_by('-rarity').values_list('rarity', flat=True).distinct()

        # this code has strange behaviour "instance duplication" when I put ordering = ['name'] in class StudentAdmin 
        # rarity_values = queryset.values_list('rarity', flat=True).distinct()
        # Details https://docs.djangoproject.com/en/5.0/ref/models/querysets/#django.db.models.query.QuerySet.distinct

        # Filter out options with zero items
        return [(str(rarity), f"{'★' * rarity}") for rarity in rarity_values if queryset.filter(rarity=rarity).exists()]
    
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(rarity=value)

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_student_names']
    ordering = ['name'] 

    def get_student_names(self, obj):
        name_list = [student.name for student in obj.student_set.all().order_by('name')]
        name_list = list(dict.fromkeys(name_list))
        return ', '.join(name_list)

    get_student_names.short_description = 'Students'

class VersionAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_student_images']
    ordering = ['id']

    def display_student_images(self, obj):
        students = obj.student_set.all().order_by('name')
        context = {
            'students': students
        }
        return render_to_string('admin/student_version.html', context)

    display_student_images.short_description = 'Students'

    class Media:
        css = {
            'all': ('/static/css/admin_banner.css',),
        }

class StudentAdmin(admin.ModelAdmin):
    # Set form
    form = StudentAdminForm
    
    # Set field
    list_display = ['portrait', 'name', 'version', 'rarity', 'school', 'is_limited', 'edit_button']
    list_per_page = 10
    ordering = ['name']

    # Set search and filtering
    show_facets = admin.ShowFacets.ALWAYS
    search_fields = ['name']
    list_filter = [RarityFilter, 'school', 'version', 'is_limited']

    # Custom field
    def portrait(self, obj):
        name = obj.name
        version = obj.version_name
        image_url = obj.image.url
        context = {
            'name': name,
            'version': version,
            'image_url': image_url,
        }
        return render_to_string('admin/student_portrait.html', context)

    def edit_button(self, obj):
        app = obj._meta.app_label
        model = obj._meta.model_name
        edit_url = reverse(f'admin:{app}_{model}_change',  args=[obj.id])
        context = {
            'edit_url': edit_url
        }
        return render_to_string('admin/edit_button.html', context)
    
    edit_button.short_description = ''

    class Media:
        css = {
            'all': ('/static/css/admin_student.css',),
        }

admin.site.register(Student, StudentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Version, VersionAdmin)