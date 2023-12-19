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
    list_per_page = 10
    ordering = ['name']

    # Set search and filtering
    show_facets = admin.ShowFacets.ALWAYS
    search_fields = ['name']
    list_filter = [RarityFilter, 'school', 'version', 'is_limited']

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
    list_display = ['name', 'is_pickup_img','not_pickup_img']
    list_per_page = 1
    filter_horizontal = ('is_pickup', 'not_pickup')

    def get_student_images_html(self, students, rarity_symbol):

        images_html = [
            f'<div style="margin-bottom: 5px">'
            f'<img src="{student.image.url}" alt="{student.name}_{student.version}" style="height:80px;">'
            f'<figcaption>{student.name}{("_" + student.version if student.version != "Original" else "")}</figcaption>\n'
            f'</div>'
            for student in students
        ]
        
        html = [
            f'<div><h3>{rarity_symbol}</h3>'
            f'<div style="justify-content: left;">'
            f'<figure style="display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); text-align: center;">'
            f'{''.join(images_html)}'
            f'</figure>'
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
    
admin.site.register(Student, StudentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(GachaBanner, GachaBannerAdmin)