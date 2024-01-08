import os
from PIL import Image
from django.db import models
from django.core.exceptions import ValidationError

def student_portrait_path(instance, filename):
    name = instance.name
    version = instance.version if instance.version != 'Original' else ''
    extension = os.path.splitext(filename)[1]
    filename = f'{name}_{version}_150{extension}'
    return os.path.join('image/student/portrait/', filename)

def school_logo_path(instance, filename):
    name = instance.name
    extension = os.path.splitext(filename)[1]
    filename = f'{name}{extension}'
    return os.path.join('image/school/logo/', filename)

class Version(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    image = models.ImageField(upload_to=school_logo_path, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        try:
            old_instance = School.objects.get(pk=self.pk)
            old_image = old_instance.image
            if old_image and old_image != self.image and os.path.isfile(old_image.path):
                os.remove(old_image.path)

        except School.DoesNotExist:
            pass

        super(School, self).save(*args, **kwargs)
    
        if self.image:
            img = Image.open(self.image.path)
            img_width, img_height = img.size
            new_height = 150.0
            percentage = (new_height / float(img_height))
            new_width = int((float(img_width) * float(percentage)))
            img.thumbnail((new_width, new_height))
            img.save(self.image.path)
    
class Student(models.Model):
    name = models.CharField(max_length=100, blank=False)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    rarity = models.PositiveIntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★')])
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    is_limited = models.BooleanField(default=False)
    image = models.ImageField(upload_to=student_portrait_path, blank=True, null=True)

    @property
    def version_name(self):
        return self.version.name
    
    @property
    def school_name(self):
        return self.school.name

    def __str__(self):
        limited = "_Limited" if self.is_limited else ""
        return f'{self.name}_{self.version_name}_{self.rarity}{limited}'
    
    def save(self, *args, **kwargs):
        try:
            old_instance = Student.objects.get(pk=self.pk)
            old_image = old_instance.image
            if old_image and old_image != self.image and os.path.isfile(old_image.path):
                os.remove(old_image.path)

        except Student.DoesNotExist:
            pass

        super(Student, self).save(*args, **kwargs)
    
        if self.image:
            img = Image.open(self.image.path)
            img_width, img_height = img.size
            new_height = 150.0
            percentage = (new_height / float(img_height))
            new_width = int((float(img_width) * float(percentage)))
            img.thumbnail((new_width, new_height))
            img.save(self.image.path)

    def clean(self):
        query = Student.objects.exclude(pk=self.pk)
        existing_student = query.filter(name=self.name).first()
        if existing_student and existing_student.school != self.school:
            raise ValidationError({'name': f'A student \'{self.name}\' already exists in \'{existing_student.school_name}\' but you select \'{self.school_name}\'.'})

    class Meta:
        unique_together = ('name', 'version')

