import os
from django.db import models
from django.contrib.auth import get_user_model
from student_app.models import Student

# def achievement_icon_path(instance, filename):
#     name = instance.id
#     extension = os.path.splitext(filename)[1]
#     filename = f'{str(name).zfill(3)}{extension}'
#     return os.path.join('image/achievement/', filename)

class Achievement(models.Model):
    achievement_id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name='ID')
    achievement_name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Name')
    achievement_description = models.TextField(blank=True, null=True, verbose_name='Description')
    achievement_criteria = models.ManyToManyField(Student, related_name='criteria', blank=True, verbose_name='Requirements')
    achievement_image = models.BinaryField(null=True, verbose_name='Icon')

    def __str__(self) -> str:
        return self.achievement_name
    
    @property
    def id(self) -> int:
        return self.achievement_id
    
    @property
    def name(self) -> str:
        return self.achievement_name
    
    @property
    def description(self) -> str:
        return self.achievement_description
    
    ### fix later
    # @property
    # def criteria(self) -> list:
    #     return self.achievement_criteria.all()

    @property
    def image(self) -> bytes:
        return self.achievement_image
    
    class Meta:
        db_table = 'achievement_table'
    
# class Achievement_OLD(models.Model):
#     name = models.CharField(max_length=100, unique=True, blank=False)
#     description = models.TextField(blank=True, null=True)
#     criteria = models.ManyToManyField(Student, related_name='criteria', blank=True)
#     image = models.ImageField(upload_to=achievement_icon_path, blank=True, null=True)

#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         try:
#             old_image = Achievement.objects.get(pk=self.pk).image
#             if old_image and old_image != self.image and os.path.isfile(old_image.path):
#                 os.remove(old_image.path)

#         except Achievement.DoesNotExist:
#             old_image = None

#         super(Achievement, self).save(*args, **kwargs)
    
#         if self.image:
#             img = Image.open(self.image.path)
#             img_width, img_height = img.size
#             max_height = 150.0
#             height_percent = (max_height / float(img_height))
#             new_width = int((float(img_width) * float(height_percent)))
#             output_size = (new_width, max_height)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

class ObtainedAchievement(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.datetime.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return f'{self.user.username} unlock {self.achievement.name}'
    
    class Meta:
        unique_together = ['user', 'achievement']

class ObtainedStudent(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.datetime.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together = ['user', 'student']