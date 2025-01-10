from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.template.loader import render_to_string

from .models import Student, School, Version
from .forms import StudentAdminForm, SchoolAdminForm, VersionAdminForm

class RarityFilter(admin.SimpleListFilter):
    title = "rarity"
    parameter_name = "rarity"

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        rarity_values = queryset.order_by('-student_rarity').values_list('student_rarity', flat=True).distinct()

        # this code has strange behaviour "instance duplication" when I put ordering = ['name'] in class StudentAdmin 
        # rarity_values = queryset.values_list('rarity', flat=True).distinct()
        # Details https://docs.djangoproject.com/en/5.0/ref/models/querysets/#django.db.models.query.QuerySet.distinct

        # Filter out options with zero items
        return [(str(rarity), f"{'★' * rarity}") for rarity in rarity_values if queryset.filter(student_rarity=rarity).exists()]
    
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(student_rarity=value)

class SchoolAdmin(admin.ModelAdmin):
    form = SchoolAdminForm
    list_display = ['school_id', 'school_name', 'school_logo']
    ordering = ['school_name'] 

    def school_logo(self, obj:School):
        context = { 
            'school_id': obj.pk,
            'school_name': obj.name,
        }
        print(context)
        return render_to_string('admin/school_logo.html', context)

    # class Media:
    #     css = {
    #         'all': ('/static/css/admin-overrides.css',),
    #     }

class VersionAdmin(admin.ModelAdmin):
    form = VersionAdminForm
    list_display = ['version_id', 'version_name', 'display_student_images']
    ordering = ['version_name'] 

    def school_logo(self, obj:Version):
        context = { 'school_id ': obj.pk }
        return render_to_string('admin/school_logo.html', context)
    
    def display_student_images(self, obj:Version):
        students = obj.student_set.all().order_by('student_name')
        context = { 'students': students }
        return render_to_string('admin/student_version.html', context)
    
    display_student_images.short_description = 'Students'

class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ['student_id', 'student_portrait', 'student_name', 'version_id', 'student_rarity', 'school_id', 'student_is_limited', 'edit_button']
    list_per_page = 10
    ordering = ['student_name']

    show_facets = admin.ShowFacets.ALWAYS
    search_fields = ['name']
    list_filter = [RarityFilter, 'school_id', 'version_id', 'student_is_limited']

    def student_portrait(self, obj:Student):
        context = {
            'student_id': obj.pk,
            'student_name': f"{obj.name} {obj.version}"
        }
        return render_to_string('admin/student_portrait.html', context)

    def edit_button(self, obj):
        app = obj._meta.app_label
        model = obj._meta.model_name
        edit_url = reverse(f'admin:{app}_{model}_change',  args=[obj.id])
        context = { 'edit_url': edit_url }
        return render_to_string('admin/edit_button.html', context)

    student_portrait.short_description = 'Portrait'
    edit_button.short_description = ''

admin.site.register(Student, StudentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Version, VersionAdmin)