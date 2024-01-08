import os
from PIL import Image

class ImageProcessor:
    @staticmethod
    def resize_by_height(resolution, source, destination):
        img = Image.open(source)
        img_width, img_height = img.size
        max_height = resolution
        percentage = (max_height / float(img_height))
        new_width = int((float(img_width) * float(percentage)))
        img.thumbnail((new_width, max_height))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        img.save(destination)

    @staticmethod
    def resize_by_width(resolution, source, destination):
        img = Image.open(source)
        img_width, img_height = img.size
        max_width = resolution
        percentage = (max_width / float(img_width))
        new_height = int((float(img_height) * float(percentage)))
        img.thumbnail((max_width, new_height))
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        img.save(destination)