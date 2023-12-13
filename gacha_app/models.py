import os
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image

def image_upload_path(instance, filename):
    version_str = f'_({instance.version})' if instance.version != 'Original' else ''
    filename = f'{instance.name}{version_str}_150{os.path.splitext(filename)[1]}'
    return os.path.join('portrait/', filename)

class School(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)

    def get_student_names(self):
        return ', '.join(sorted(set(student.name for student in self.student_set.all())))

    def __str__(self):
        return self.name
    
class Student(models.Model):
    name = models.CharField(max_length=100, blank=False)
    version = models.CharField(max_length=50, blank=False, default='Original')
    rarity = models.PositiveIntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★')])
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    is_limited = models.BooleanField(default=False)
    image = models.ImageField(upload_to=image_upload_path, blank=True, null=True)

    def __str__(self):
        return f'{self.name}_{self.version}'
    
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
            existing_student = Student.objects.exclude(pk=self.pk).get(name=self.name)
            if existing_student.school != self.school:
                raise ValidationError({'name': f'A student \'{self.name}\' already exists in \'{existing_student.school}\' but you select \'{self.school}\'.'})
        except Student.DoesNotExist:
            pass

    class Meta:
        unique_together = ('name', 'version')


    
class GachaBanner(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    rate_3_star = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    rate_2_star = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    rate_1_star = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    is_pickup = models.ManyToManyField('Student', related_name='pickup', blank=True)
    not_pickup = models.ManyToManyField('Student', related_name='not_pickup', blank=True)

    def clean(self):
        # Ensure that the sum of rates is equal to 100%
        print(self.rate_3_star, self.rate_2_star, self.rate_1_star)
        print(self.is_pickup.all())
        total_rate = self.rate_3_star + self.rate_2_star + self.rate_1_star
        if total_rate != 100.0:
            raise ValidationError("MODEL The sum of rates must equal 100%.")
        

    def __str__(self):
        return self.name