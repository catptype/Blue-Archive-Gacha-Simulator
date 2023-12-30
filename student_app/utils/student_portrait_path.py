import os

def student_portrait_path(instance, filename):
    name = instance.name
    version = instance.version if instance.version != 'Original' else ''
    extension = os.path.splitext(filename)[1]
    filename = f'{name}_{version}_150{extension}'
    return os.path.join('image/student/portrait/', filename)