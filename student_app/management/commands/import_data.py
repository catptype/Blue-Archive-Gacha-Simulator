import json
import os
from django.core.management.base import BaseCommand
from student_app.models import Version, School, Student
from django.conf import settings
from PIL import Image

class Command(BaseCommand):
    help = 'Load data from JSON files into model'
    def handle(self, *args, **options):
        self.import_versions()
        self.import_schools()
        self.import_students_r1()
        self.import_students_r2()
        self.import_students_r3()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    
    def student_portrait_processing(self, source, destination):
        img = Image.open(source)
        img_width, img_height = img.size
        max_height = 150.0
        height_percent = (max_height / float(img_height))
        new_width = int((float(img_width) * float(height_percent)))
        output_size = (new_width, max_height)
        img.thumbnail(output_size)
        img.save(destination)

    def import_schools(self):
        with open('student_app/data/json/version.json') as file:
            versions = json.load(file)
            for data in versions:
                name = data['name']
                if not Version.objects.filter(name=name).exists():
                    Version.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'Import {name} to School model'))

    def import_versions(self):
        with open('student_app/data/json/school.json') as file:
            schools = json.load(file)
            for data in schools:
                name = data['name']
                if not School.objects.filter(name=name).exists():
                    School.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'Import {name} to Version model'))

    def import_students_r1(self):
        with open('student_app/data/json/student_r1.json') as file:
            students_r1 = json.load(file)
            for data in students_r1:
                name = data['name']
                version = Version.objects.get(name=data['version'])
                school = School.objects.get(name=data['school'])
                image_json = data['image']

                if not Student.objects.filter(name=name, version=version).exists():
                    
                    image_source_path = os.path.join(settings.BASE_DIR, 'student_app', 'data', image_json)
                    extension = os.path.splitext(image_source_path)[1]
                    image_model_path = os.path.join('image', 'student', 'portrait', f'{name}_{version}_150{extension}')
                    image_media_path = os.path.join(settings.MEDIA_ROOT, image_model_path)

                    # Resize Image
                    self.student_portrait_processing(image_source_path, image_media_path)
                    
                    Student.objects.create(
                        name=name,
                        version=version,
                        rarity=1,
                        school=school,
                        is_limited=False,
                        image=image_model_path
                    )
                    self.stdout.write(self.style.SUCCESS(f'Import {name}_{data['version']} to Student model'))

    def import_students_r2(self):
        with open('student_app/data/json/student_r2.json') as file:
            students_r2 = json.load(file)
            for data in students_r2:
                name = data['name']
                version = Version.objects.get(name=data['version'])
                school = School.objects.get(name=data['school'])
                image_json = data['image']

                if not Student.objects.filter(name=name, version=version).exists():
                    
                    image_source_path = os.path.join(settings.BASE_DIR, 'student_app', 'data', image_json)
                    extension = os.path.splitext(image_source_path)[1]
                    image_model_path = os.path.join('image', 'student', 'portrait', f'{name}_{version}_150{extension}')
                    image_media_path = os.path.join(settings.MEDIA_ROOT, image_model_path)

                    # Resize Image
                    self.student_portrait_processing(image_source_path, image_media_path)
                    
                    Student.objects.create(
                        name=name,
                        version=version,
                        rarity=2,
                        school=school,
                        is_limited=False,
                        image=image_model_path
                    )
                    self.stdout.write(self.style.SUCCESS(f'Import {name}_{data['version']} to Student model'))
    
    def import_students_r3(self):
        with open('student_app/data/json/student_r3.json') as file:
            students_r3 = json.load(file)
            for data in students_r3:
                name = data['name']
                version = Version.objects.get(name=data['version'])
                school = School.objects.get(name=data['school'])
                is_limited = data['is_limited']
                image_json = data['image']

                if not Student.objects.filter(name=name, version=version).exists():
                    
                    image_source_path = os.path.join(settings.BASE_DIR, 'student_app', 'data', image_json)
                    extension = os.path.splitext(image_source_path)[1]
                    image_model_path = os.path.join('image', 'student', 'portrait', f'{name}_{version}_150{extension}')
                    image_media_path = os.path.join(settings.MEDIA_ROOT, image_model_path)

                    # Resize Image
                    self.student_portrait_processing(image_source_path, image_media_path)
                    
                    Student.objects.create(
                        name=name,
                        version=version,
                        rarity=3,
                        school=school,
                        is_limited=is_limited,
                        image=image_model_path
                    )
                    self.stdout.write(self.style.SUCCESS(f'Import {name}_{data['version']} to Student model'))