import json
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from student_app.models import Version, School, Student
from .utils.Converter import Converter
from .utils.TextProgressBar import TextProgressBar

class Command(BaseCommand):
    help = 'Import data from JSON files into model'
    def handle(self, *args, **options):
        base_path = os.path.join(settings.BASE_DIR, 'model_script', 'data', 'json')

        student_json = os.path.join(base_path, 'student.json')
        school_json = os.path.join(base_path, 'school.json')

        self.stdout.write(self.style.SUCCESS('Start unpack'))

        self.unpack_school(school_json)
        self.unpack_student(student_json)

        self.stdout.write(self.style.SUCCESS('Data unpack complete'))

    def unpack_school(self, json_file):

        with open(json_file) as file:
            data_list = json.load(file)
            
            data_count = len(data_list)
            self.stdout.write(self.style.NOTICE(f'Unpacking {data_count} school records...'))
            prog_bar = TextProgressBar(data_count)
            
            for data in data_list:
                school_name = data['name']
                school_image_bytes = Converter.base64_to_byte(data['image_base64'])

                try:
                    school_obj:School = School.objects.get(school_name=school_name)

                    # Check if the existing school's image is different
                    if school_obj.image != school_image_bytes:
                        school_obj.school_image = school_image_bytes
                        school_obj.save()
                            
                except ObjectDoesNotExist:
                    School.objects.create(
                        school_name=school_name,
                        school_image=school_image_bytes,
                    )

                prog_bar.add_step()

        self.stdout.write(self.style.SUCCESS(f'\nUnpack school data total {data_count}'))

    def unpack_student(self, json_file):

        with open(json_file) as file:
            data_list = json.load(file)
            
            data_count = len(data_list)
            self.stdout.write(self.style.NOTICE(f'Unpacking {data_count} student records...'))
            prog_bar = TextProgressBar(data_count)
            
            for data in data_list:
                student_name = data['name']
                student_version = data['version']
                student_school = data['school']
                student_rarity = data['rarity']
                student_image_bytes = Converter.base64_to_byte(data['image_base64'])
                student_is_limited = data['is_limited']

                try:
                    version_obj:Version = Version.objects.get(version_name=student_version)
                except ObjectDoesNotExist:
                    version_obj:Version = Version.objects.create(version_name=student_version)

                try:
                    student_obj:Student = Student.objects.get(
                        student_name=student_name,
                        version_id=version_obj,
                    )

                    # Track if any changes are made
                    changes = {
                        'school_id': School.objects.get(school_name=student_school),
                        'student_image': student_image_bytes,
                        'student_rarity': student_rarity,
                        'student_is_limited': student_is_limited,
                    }

                    # Check for changes and update the student object only if necessary
                    is_change = False
                    for field, new_value in changes.items():
                        if getattr(student_obj, field) != new_value:
                            setattr(student_obj, field, new_value)
                            is_change = True

                    if is_change:    
                        student_obj.save()

                except ObjectDoesNotExist:
                    Student.objects.create(
                        student_name=student_name,
                        version_id=version_obj,
                        student_rarity=student_rarity,
                        school_id=School.objects.get(school_name=student_school),
                        student_image=student_image_bytes,
                        student_is_limited=student_is_limited,
                    )
                
                prog_bar.add_step()
        
        self.stdout.write(self.style.SUCCESS(f'\nUnpack student data total {data_count}'))

