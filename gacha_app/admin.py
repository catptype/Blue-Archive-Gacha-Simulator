from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Student, School, GachaBanner
from .forms import StudentAdminForm, GachaBannerAdminForm

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
        return obj.get_student_names()

    get_student_names.short_description = 'members'  # Optional:

class StudentAdmin(admin.ModelAdmin):
    # Set form
    form = StudentAdminForm
    
    # Set field
    list_display = ['image_tag', 'name', 'version', 'rarity', 'school', 'is_limited', 'edit_button']
    ordering = ['name']

    # Set search and filtering
    show_facets = admin.ShowFacets.ALWAYS
    search_fields = ['name']
    list_filter = [RarityFilter, 'version', 'is_limited']
    
    # Custom field
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

class GachaBannerAdmin(admin.ModelAdmin):
    form = GachaBannerAdminForm
    list_display = ['name', 'pickup_list', 'not_pickup_list']

    def pickup_list(self, obj):
        return ", ".join([student.name for student in obj.is_pickup.all()])


    def not_pickup_list(self, obj):
        return ", ".join([student.name for student in obj.not_pickup.all()])

    pickup_list.short_description = 'Pickup'
    not_pickup_list.short_description = 'Not pickup'


    
admin.site.register(Student, StudentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(GachaBanner, GachaBannerAdmin)