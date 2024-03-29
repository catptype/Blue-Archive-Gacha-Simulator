import json
import os
from PIL import Image
from django.conf import settings
from django.core.management.base import BaseCommand
from student_app.models import Version, School, Student
from gacha_app.models import GachaType, GachaBanner
from user_app.models import Achievement
from .utils import ImageProcessor

class Command(BaseCommand):
    help = 'Import data from JSON files into model'
    def handle(self, *args, **options):
        basepath = os.path.join(settings.BASE_DIR, 'model_script', 'data', 'json')

        student_json_list = [
            'student_r1.json',
            'student_r2.json',
            'student_r3.json'
        ]

        achievement_json_list = [
            'achievement_abydos.json',
            'achievement_arius.json',
            'achievement_gehenna.json',
            'achievement_hyakkiyako.json',
            'achievement_millennium.json',
            'achievement_redwinter.json',
            'achievement_shanhaijing.json',
            'achievement_SRT.json',
            'achievement_trinity.json',
            'achievement_alternative.json',
            'achievement_unique.json',
        ]

        self.import_versions(os.path.join(basepath, 'student_version.json'))
        self.import_schools(os.path.join(basepath, 'school.json'))
        self.import_gachatype(os.path.join(basepath, 'gacha_type.json'))
        self.import_banner(os.path.join(basepath, 'gacha_banner.json'))

        for json_file in student_json_list:
            self.import_students(os.path.join(basepath, json_file))

        for json_file in achievement_json_list:            
            self.import_achievement(os.path.join(basepath, json_file))
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

    def achievement_icon_processing(self, source, destination):
        img = Image.open(source)
        img_width, img_height = img.size
        max_height = 150.0
        height_percent = (max_height / float(img_height))
        new_width = int((float(img_width) * float(height_percent)))
        output_size = (new_width, max_height)
        img.thumbnail(output_size)
        img.save(destination)

    def import_achievement(self, json_file):
        with open(json_file) as file:
            achievements = json.load(file)
            for data in achievements:
                name = data['name']
                description = data['description']
                
                if not Achievement.objects.filter(name=name).exists():
                    # TO-DO Implement image later
                    # image_source_path = os.path.join(settings.BASE_DIR, 'model_script', 'data', image_json)
                    # extension = os.path.splitext(image_source_path)[1]
                    # image_model_path = os.path.join('image', 'achievement', f'{name}{extension}')
                    # image_media_path = os.path.join(settings.MEDIA_ROOT, image_model_path)

                    # Resize Image
                    # ImageProcessor.resize_by_width(150.0, image_source_path, image_media_path)

                    achievement = Achievement.objects.create(
                        name=name,
                        description=description,
                    )
                    
                    criteria_list = data['criteria']
                    for criteria in criteria_list:
                        version = Version.objects.get(name=criteria['version'])
                        student = Student.objects.get(name=criteria['student'], version=version)
                        achievement.criteria.add(student)

                    self.stdout.write(self.style.SUCCESS(f'Import {name} to Achievement model'))

    def import_banner(self, json_file):
        with open(json_file) as file:
            banners = json.load(file)
            for data in banners:
                name = data['name']
                banner_type = GachaType.objects.get(name=data['banner_type'])
                if not GachaBanner.objects.filter(name=name).exists():
                    GachaBanner.objects.create(
                        name=name,
                        banner_type=banner_type,
                    )
                    self.stdout.write(self.style.SUCCESS(f'Import {name} to GachaBanner model'))

    def import_gachatype(self, json_file):
        with open(json_file) as file:
            types = json.load(file)
            for data in types:
                name = data['name']
                if not GachaType.objects.filter(name=name).exists():
                    GachaType.objects.create(
                        name=name,
                        feature_rate=data['feature_rate'],
                        r3_rate=data['r3_rate'],
                        r2_rate=data['r2_rate'],
                        r1_rate=data['r1_rate'],
                    )
                    self.stdout.write(self.style.SUCCESS(f'Import {name} to GachaType model'))

    def import_schools(self, json_file):
        with open(json_file) as file:
            versions = json.load(file)
            for data in versions:
                name = data['name']
                image_json = data['image']
                if not School.objects.filter(name=name).exists():
                    image_source_path = os.path.join(settings.BASE_DIR, 'model_script', 'data', image_json)
                    extension = os.path.splitext(image_source_path)[1]
                    image_model_path = os.path.join('image', 'school', 'logo', f'{name}{extension}')
                    image_media_path = os.path.join(settings.MEDIA_ROOT, image_model_path)

                    # Resize Image
                    ImageProcessor.resize_by_height(150.0, image_source_path, image_media_path)

                    School.objects.create(
                        name=name,
                        image=image_model_path,
                    )
                    self.stdout.write(self.style.SUCCESS(f'Import {name} to School model'))

    def import_versions(self, json_file):
        with open(json_file) as file:
            schools = json.load(file)
            for data in schools:
                name = data['name']
                if not Version.objects.filter(name=name).exists():
                    Version.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f'Import {name} to Version model'))

    def import_students(self, json_file):
        with open(json_file) as file:
            students = json.load(file)
            for data in students:
                name = data['name']
                version = Version.objects.get(name=data['version'])
                school = School.objects.get(name=data['school'])
                rarity = data['rarity']
                is_limited = data['is_limited']
                image_json = data['image']
                if not Student.objects.filter(name=name, version=version).exists():                    
                    image_source_path = os.path.join(settings.BASE_DIR, 'model_script', 'data', image_json)
                    extension = os.path.splitext(image_source_path)[1]
                    image_model_path = os.path.join('image', 'student', 'portrait', f'{name}_{version}_150{extension}')
                    image_media_path = os.path.join(settings.MEDIA_ROOT, image_model_path)

                    # Resize Image
                    ImageProcessor.resize_by_height(150.0, image_source_path, image_media_path)
                    
                    Student.objects.create(
                        name=name,
                        version=version,
                        rarity=rarity,
                        school=school,
                        is_limited=is_limited,
                        image=image_model_path
                    )
                    self.stdout.write(self.style.SUCCESS(f'Import {name}_{data['version']} to Student model'))