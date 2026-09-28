from PIL import Image
from PIL.ExifTags import TAGS

def get_photo_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag == "DateTime":
                return value

    except Exception as e:
        print(f"오류 발생 : {e}")

    return None


date = get_photo_date("test_image/20250117_103910.jpg")
print(date)