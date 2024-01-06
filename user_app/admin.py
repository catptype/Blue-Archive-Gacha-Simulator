from django.contrib import admin
from django.template.loader import render_to_string

from .forms import AchievementAdminForm
from .models import Achievement, ObtainedAchievement, ObtainedStudent

class AchievementAdmin(admin.ModelAdmin):
    form = AchievementAdminForm
    list_display = ['name', 'description', 'criteria_students']

    def criteria_students(self, obj):
        students = obj.criteria.all().order_by('name')
        context = {
            'students': students,
        }
        return render_to_string('admin/criteria_student.html', context)
    
    class Media:
        css = {
            'all': ('/static/css/admin-overrides.css',),
        }

class ObtainedAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'datetime']

class ObtainedStudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'student', 'datetime']

admin.site.register(Achievement, AchievementAdmin)
admin.site.register(ObtainedAchievement, ObtainedAchievementAdmin)
admin.site.register(ObtainedStudent, ObtainedStudentAdmin)