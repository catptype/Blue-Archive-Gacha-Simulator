from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from student_app.models import Student

FIXED_TIMEZONE = 420

class GachaRatePreset(models.Model):
    preset_id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name='ID')
    preset_name = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name='Preset name')
    preset_feature_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False, verbose_name='Feature rate')
    preset_r3_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False, verbose_name='★★★ rate')
    preset_r2_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False, verbose_name='★★ rate')
    preset_r1_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=False, verbose_name='★ rate')

    def __str__(self) -> str:
        return f"[{self.id:03d}] {self.name} ({self.feature}) {self.r3}-{self.r2}-{self.r1}"

    @property
    def id(self) -> int:
        return self.preset_id

    @property
    def name(self) -> str:
        return self.preset_name
    
    @property
    def feature(self) -> float:
        return self.preset_feature_rate
    
    @property
    def r3(self) -> float:
        return self.preset_r3_rate
    
    @property
    def r2(self) -> float:
        return self.preset_r2_rate
    
    @property
    def r1(self) -> float:
        return self.preset_r1_rate

    class Meta:
        db_table = 'gacha_rate_preset'

class GachaBanner(models.Model):
    banner_id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name='ID')
    banner_name = models.CharField(max_length=100, unique=True, blank=False, null=False, verbose_name='Banner name')
    banner_image = models.BinaryField(null=True, verbose_name='Banner image')
    preset_id = models.ForeignKey(GachaRatePreset, on_delete=models.CASCADE)
    banner_pickup = models.ManyToManyField(Student, related_name='pickup', blank=True)
    banner_non_pickup = models.ManyToManyField(Student, related_name='not_pickup', blank=True)

    def __str__(self) -> str:
        return f"[{self.id:03d}] {self.name}"
    
    @property
    def id(self) -> int:
        return self.banner_id
    
    @property
    def name(self) -> str:
        return self.banner_name

    @property
    def pickup(self) -> Student:
        return self.banner_pickup
    
    @property
    def non_pickup(self) -> Student:
        return self.banner_non_pickup

    class Meta:
        db_table = 'gacha_banner'

class GachaTransaction(models.Model):
    transaction_id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name='ID')
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    banner_id = models.ForeignKey(GachaBanner, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    transaction_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"[{self.id:06d}]"
    
    @property
    def id(self) -> int:
        return self.transaction_id
    
    @property
    def user(self) -> str:
        return self.user_id.username
    
    @property
    def banner_name(self) -> str:
        return self.banner_id.name
    
    @property
    def student(self):
        return self.student_id.fullname
    
    @property
    def datetime(self):
        utc_time = self.transaction_datetime
        local_time = timezone.localtime(utc_time, timezone=timezone.get_fixed_timezone(FIXED_TIMEZONE))
        return local_time.strftime("%B %d, %Y, %I:%M %p")

    class Meta:
        db_table = 'gacha_transaction'
