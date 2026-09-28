from PIL import Image
from PIL.ExifTags import TAGS

image_path = "test_image/20250117_103910.jpg"

image = Image.open(image_path)
exif_data = image.getexif()

for tag_id, value in exif_data.items():
    tag = TAGS.get(tag_id, tag_id)
    print(f"{tag}: {value}")
