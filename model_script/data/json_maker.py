import os
import json
import base64
from PIL import Image
from io import BytesIO

from util.DirectoryProcessor import DirectoryProcessor
from util.Converter import Converter

OUTPUT_DIR = r"json"
DirectoryProcessor.create_dir(OUTPUT_DIR)

IMAGE_PACK = {
    'r1': DirectoryProcessor.get_all_files(r"image\r1"),
    'r2': DirectoryProcessor.get_all_files(r"image\r2"),
    'r3': DirectoryProcessor.get_all_files(r"image\r3"),
    'r3_limited': DirectoryProcessor.get_all_files(r"image\r3_limited"),
    'school': DirectoryProcessor.get_all_files(r"image\school"),
}

STUDENT_SCHOOL = {
    'Abydos': ['Hoshino', 'Nonomi', 'Serika', 'Shiroko', 'Ayane'],
    'Arius': ['Atsuko', 'Hiyori', 'Misaki', 'Saori'],
    'Gehenna': [
        'Akari', 'Haruna', 'Izumi', 'Junko',     # Food Research
        'Ako', 'Chinatsu', 'Hina', 'Iori',      # Problem Solver
        'Aru', 'Haruka', 'Kayoko', 'Mutsuki',   # Benriya 68
        'Chiaki', 'Iroha', 'Satsuki', 'Makoto', 'Ibuki',    # Pandemonium Society
        'Kasumi', 'Megu',                       # Onsen
        'Kirara', 'Erika',                      # Go home club
        'Sena',                                 # Medic?
        'Fuuka', 'Juri',                        # Lunch maker
    ],
    'Hyakkiyako': [
        'Izuna', 'Tsukuyo', 'Michiru',  # Ninja
        'Kaede', 'Mimori', 'Tsubaki',   # Inner Discipline
        'Chise', 'Kaho', 'Niya',        # Yin-Yang
        'Kikyou', 'Renge', 'Yukari',    # Hyakkaryouran
        'Umika', 'Shizuko', 'Pina',     # Festival Operations Department
        'Wakamo',                       # Other
    ],
    'Millennium': [
        'Rio', 'Yuuka', 'Noa', 'Koyuki', # Seminar
        'Akane', 'Asuna', 'Karin', 'Toki', 'Neru',        # C&C
        'Arisu', 'Midori', 'Momoi', 'Yuzu',        # Game dev
        'Chihiro', 'Hare', 'Maki', 'Kotama',       # Verita
        'Utaha', 'Hibiki', 'Kotori',            # Engineer
        'Himari', 'Eimi',       # Supernatsural Phenomenon Task Force
        'Sumire', 'Rei',        # Training
    ],
    'Red Winter': [
        'Cherino', 'Marina', 'Tomoe',       # Red Winter Office
        'Nodoka', 'Shigure',    # Spec Ops 227
        'Momiji', 'Meru',       # Knowledge Liberation Front
        'Yakumo', 'Takane',     # Publishing Department
        'Minori',               # Labor Party
    ],
    'Shanhaijing': [
        'Kisaki', 'Mina',       # Genryumon
        'Rumi', 'Reijo',        # Black Tortoise Promenade
        'Shun', 'Kokona',       # Plum Blossom Garden
        'Kai', 'Saya',          # Eastern Alchemy Society
        'Kaguta',               # Peking Opera
    ],
    'SRT': [
        'Miyako', 'Saki', 'Miyu', 'Moe',    # RABBIT
        'Yukino', 'Niko', 'Kurumi', 'Otogi',    # FOX
    ],
    'Trinity': [
        'Mika', 'Nagisa', 'Seia',       # Tea Party
        'Hifumi', 'Azusa', 'Hanako', 'Koharu', # Supllemental Lessons
        'Tsurugi', 'Hasumi', 'Mashiro', 'Ichika', # Justice Task
        'Sakurako', 'Hinata', 'Mari',   # Sister hood
        'Kazusa', 'Yoshimi', 'Natsu', 'Airi',    # After School Sweets
        'Mine', 'Serina', 'Hanae',      # Remedial Knights
        'Suzumi', 'Reisa',              # Vigilante Crew
        'Ui', 'Shimiko',                # Library Committee
    ],
    'Valkyrie': [ 'Kanna', 'Konoka', 'Kirino', 'Fubuki' ],
}

def generate_base64(image_path):
    # image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image_base64 = Converter.cv2_to_base64(image)
    # return image_base64

    with Image.open(image_path) as img:
        # Ensure the image is in RGBA mode
        img = img.convert("RGBA")
        
        # Save the image to a BytesIO object
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Convert the image bytes to base64
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        return img_base64

def main():
    student_list = []
    school_list = []
    
    for key, image_path_list in IMAGE_PACK.items():

        if key in ['r1', 'r2', 'r3', 'r3_limited']:
            for image_path in image_path_list:
                _, filename, _ = DirectoryProcessor.decompose_path(image_path)
                student_name, student_version = filename.split('_')
                
                student_school = None
                for school_name, student_member_list in STUDENT_SCHOOL.items():
                    if student_name in student_member_list:
                        student_school = school_name
                        break
                
                if student_school is None:
                    raise ValueError(f"'{student_name}' does not have school")
                
                student_rarity = {'r1': 1, 'r2': 2, 'r3': 3, 'r3_limited': 3 }.get(key)
                student_is_limited = key == 'r3_limited'
                image_base64 = generate_base64(image_path)
                
                data = {
                    'type': 'student',
                    'name': student_name,
                    'version': student_version,
                    'school': student_school,
                    'rarity': student_rarity,
                    'image_base64': image_base64,
                    'is_limited': student_is_limited,
                }

                student_list.append(data)
        
        elif key in ['school']:
            for image_path in image_path_list:
                _, filename, _ = DirectoryProcessor.decompose_path(image_path)

                school_name = filename
                image_base64 = generate_base64(image_path)

                data = {
                    'type': 'school',
                    'name': school_name,
                    'image_base64': image_base64,
                }

                school_list.append(data)
        
        else:
            raise KeyError(f"IMAGE_PACK keys '{key}' error")

    with open(os.path.join(OUTPUT_DIR, 'student.json'), "w") as json_file:
        json.dump(student_list, json_file, indent=4) 
    
    with open(os.path.join(OUTPUT_DIR, 'school.json'), "w") as json_file:
        json.dump(school_list, json_file, indent=4) 

if __name__ == "__main__":
    main()