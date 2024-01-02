# My note for django website project

## Step to initialize project

### preparing virtual environment
```
conda create --name env_name python=3.12
conda activate env_name
pip install django
```
### Preparing project

#### create project
```
django-admin startproject project_name
```
#### create app
```
django-admin startapp app_name
```
in `project_name/settings.py` make sure to include `app_name` in `INSTALLED_APPS` variable
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_name', <<< Add here (Method 1 simple)
    'app_name.apps.MyAppConfig', <<< Add here (Method 2 fullpath need to look at apps.py file)
]
```
#### migrate database
```
cd /path/to/your/django/project
python manage.py makemigrations
python manage.py migrate
```
#### create superuser
```
cd /path/to/your/django/project
python manage.py createsuperuser

Username (leave blank to use 'your_username'):
Email address: your_email@example.com
Password: **********
Password (again): **********
```
#### run webserver
```
cd /path/to/your/django/project
python manage.py runserver
```
## Customization

### Filter in admin page
```python
class MyModelAdmin(admin.ModelAdmin):
    show_facets = admin.ShowFacets.ALLOW  # default - when '_facets' in URL query string
    show_facets = admin.ShowFacets.ALWAYS # show always
    show_facets = admin.ShowFacets.NEVER  # always disabled
```

## Verification methods
### Based on model 
For `Blue Archive`, there are several `version` of each `student` but all `version` corressponding to the same `school`. To put them into database record. It must do self verification to confirm that new version of student have same school in database record. 
```python
# models.py
class Student(models.Model):
    name = models.CharField(max_length=100, blank=False)
    version = models.CharField(max_length=50, blank=False, default='Original')
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def clean(self):
        try:
            existing_student = Student.objects.exclude(pk=self.pk).get(name=self.name)
            if existing_student.school != self.school:
                raise ValidationError({'name': f'A student \'{self.name}\' already exists in \'{existing_student.school}\' but you select \'{self.school}\'.'})
        except Student.DoesNotExist:
            pass

```
### Based on form
In case gacha banner, it is possible to do verification summation of (`r3_rate`, `r2_rate`, and `r1_rate`) = 100 or not.

```python
# models.py
class GachaBanner(models.Model):
    name = models.CharField(max_length=100, unique=True)
    r3_rate = models.DecimalField(max_digits=5, decimal_places=1)
    r2_rate = models.DecimalField(max_digits=5, decimal_places=1)
    r1_rate = models.DecimalField(max_digits=5, decimal_places=1)
    is_pickup = models.ManyToManyField('Student', related_name='pickup', blank=True)
    not_pickup = models.ManyToManyField('Student', related_name='not_pickup', blank=True)

    def clean(self):
        # Ensure that the sum of rates is equal to 100%
        total_rate = self.r3_rate + self.r2_rate + self.r1_rate
        if total_rate != 100.0:
            raise ValidationError("The sum of rates must equal 100%.")
```

However, it is impossible to verify both `is_pickup` and `not_pickup` fields do not contain same `student_id` because of `models.ManyToManyField` field.
So, the verification will be occured in Forms instead of model.
Note, the verification summation of (`r3_rate`, `r2_rate`, and `r1_rate`) = 100 can be performed in form too.
```python
# forms.py
from .models import GachaBanner
class GachaBannerAdminForm(forms.ModelForm):
    class Meta:
        model = GachaBanner
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        r3_rate = cleaned_data.get('r3_rate')
        r2_rate = cleaned_data.get('r2_rate')
        r1_rate = cleaned_data.get('r1_rate')

        is_pickup = cleaned_data.get('is_pickup')
        not_pickup = cleaned_data.get('not_pickup')

        # Ensure that students in is_pickup and not_pickup are distinct
        common_students = is_pickup & not_pickup
        print(common_students)
        if common_students:
            raise ValidationError("The students in is_pickup and not_pickup.")

        # Ensure that the sum of rates is equal to 100%
        total_rate = r3_rate + r2_rate + r1_rate
        if total_rate != 100.0:
            raise ValidationError("The sum of rates must equal 100%.")
```
