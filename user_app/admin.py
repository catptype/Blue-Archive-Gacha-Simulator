from django.contrib import admin

from .models import Achievement, ObtainedAchievement, ObtainedStudent

class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'criteria']

class ObtainedAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'datetime']

class ObtainedStudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'student', 'datetime']

admin.site.register(Achievement, AchievementAdmin)
admin.site.register(ObtainedAchievement, ObtainedAchievementAdmin)
admin.site.register(ObtainedStudent, ObtainedStudentAdmin)