import os
from django.contrib.auth import get_user_model
from django.db import models

from student_app.models import Student

def banner_image_path(instance, filename):
    name = instance.name
    extension = os.path.splitext(filename)[1]
    filename = f'{name}{extension}'
    return os.path.join('image/banner/')

class GachaBanner(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    image = models.ImageField(upload_to=banner_image_path, blank=True, null=True)
    pickup_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    r3_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    r2_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    r1_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    is_pickup = models.ManyToManyField(Student, related_name='pickup', blank=True)
    not_pickup = models.ManyToManyField(Student, related_name='not_pickup', blank=True)

    def __str__(self):
        return self.name

class GachaTransaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    banner = models.ForeignKey(GachaBanner, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def formatted_datetime(self):
        return self.datetime.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def banner_name(self):
        return self.banner.name

    @property
    def student_name(self):
        return self.student.name

    def __str__(self):
        return f'{self.user}_{self.banner}_{self.student}'