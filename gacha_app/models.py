
from django.db import models
from student_app.models import Student
from django.contrib.auth import get_user_model

class GachaBanner(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    rate_3_star = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    rate_2_star = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    rate_1_star = models.DecimalField(max_digits=4, decimal_places=1, blank=False)
    is_pickup = models.ManyToManyField(Student, related_name='pickup', blank=True)
    not_pickup = models.ManyToManyField(Student, related_name='not_pickup', blank=True)

    def __str__(self):
        return self.name

class GachaTransaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    banner = models.ForeignKey(GachaBanner, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}_{self.banner}_{self.student}'