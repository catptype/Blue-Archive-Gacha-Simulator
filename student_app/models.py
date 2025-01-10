from django.db import models

class Version(models.Model):
    version_id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name='ID')
    version_name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='Version')

    def __str__(self):
        return f"[{self.id:03d}] {self.name}"
    
    @property
    def id(self):
        return self.version_id
    
    @property
    def name(self):
        return self.version_name
    
    class Meta:
        db_table = 'student_version_table'

class School(models.Model):
    school_id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name='ID')
    school_name = models.CharField(max_length=100, unique=True, blank=False, verbose_name='School')
    school_image = models.BinaryField(null=True, verbose_name='Logo')

    def __str__(self) -> str:
        return f"[{self.id:03d}] {self.name}"
    
    @property
    def id(self) -> int:
        return self.school_id
    
    @property
    def name(self) -> str:
        return self.school_name
    
    @property
    def image(self) -> bytes:
        return self.school_image
    
    class Meta:
        db_table = 'student_school_table'

class Student(models.Model):
    student_id = models.AutoField(primary_key=True, auto_created=True, editable=False, verbose_name='ID')
    student_name = models.CharField(max_length=100, blank=False)
    version_id = models.ForeignKey(Version, on_delete=models.CASCADE)
    student_rarity = models.PositiveIntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★')])
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    student_image = models.BinaryField(null=True, verbose_name='Portrait')
    student_is_limited = models.BooleanField(default=False)

    def __str__(self) -> str:
        if self.is_limited:
            return f"[{self.id:03d}] {self.school} {self.fullname} ★"
        else:
            return f"[{self.id:03d}] {self.school} {self.fullname}"
        
    @property
    def id(self) -> int:
        return self.student_id
    
    @property
    def fullname(self) -> int:
        if self.version.lower() == 'original':
            return self.name
        else:
            return f"{self.name} ({self.version})"
    
    @property
    def name(self) -> str:
        return self.student_name

    @property
    def version(self) -> str:
        return self.version_id.name
    
    @property
    def rarity(self) -> int:
        return self.student_rarity
    
    @property
    def school(self) -> str:
        return self.school_id.name
    
    @property
    def image(self) -> bytes:
        return self.student_image
    
    @property
    def is_limited(self) -> bool:
        return self.student_is_limited

    class Meta:
        db_table = 'student_table'
        unique_together = ('student_name', 'version_id')
