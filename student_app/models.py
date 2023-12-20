import os
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from django.utils.html import mark_safe

def image_upload_path(instance, filename):
    version_str = f'_({instance.version})' if instance.version != 'Original' else ''
    filename = f'{instance.name}{version_str}_150{os.path.splitext(filename)[1]}'
    return os.path.join('portrait/', filename)

class Version(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)

    def get_student_names(self):
        students = self.student_set.all().order_by('name')
        images_html = []
        for student in students:
            try:
                query = Student.objects.get(name=student.name, version=student.version)
                image_url = query.image.url
                images_html.extend([
                    f'<div class="student-item">'
                    f'<img src="{image_url}" alt="{student.name}" style="height: 80px">'
                    f'<figcaption>{student.name}</figcaption>'
                    f'</div>'
                ])
            except Student.DoesNotExist:
                pass

        return mark_safe(''.join(images_html))

    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)

    def get_student_names(self):
        return ', '.join(sorted(set(student.name for student in self.student_set.all())))

    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=100, blank=False)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    rarity = models.PositiveIntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★')])
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    is_limited = models.BooleanField(default=False)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    def __str__(self):
        limited = "_Limied" if self.is_limited else ""
        version = f"_{self.version}" if self.version != "Original" else ""
        return f'{self.name}{version}_{self.rarity}{limited}'
    
    def save(self, *args, **kwargs):
        try:
            # Get the old instance to compare the images
            old_instance = Student.objects.get(pk=self.pk)
            old_image = old_instance.image
            if old_image and old_image != self.image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)

        except Student.DoesNotExist:
            old_image = None
        
        super(Student, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            img_width, img_height = img.size
            max_height = 150.0
            height_percent = (max_height / float(img_height))
            new_width = int((float(img_width) * float(height_percent)))
            output_size = (new_width, max_height)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def clean(self):
        try:
            existing_student = Student.objects.exclude(pk=self.pk).get(name=self.name, version=self.version)
            if existing_student.school != self.school:
                raise ValidationError({'name': f'A student \'{self.name}\' already exists in \'{existing_student.school}\' but you select \'{self.school}\'.'})
        except Student.DoesNotExist:
            pass
        except Student.MultipleObjectsReturned:
            raise ValidationError(f'A duplicate student entry was found. ({self.name}_{self.version})')

    class Meta:
        unique_together = ('name', 'version')

