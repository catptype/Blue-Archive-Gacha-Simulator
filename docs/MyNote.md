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
```
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
