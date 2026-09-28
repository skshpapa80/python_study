import os
import shutil
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS


SOURCE_DIR = r"D:\Project\Python\Photo\test_image"


def get_photo_date(image_path):
    """
    EXIF에서 촬영 날짜 추출
    """
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id)

            if tag == "DateTime":
                return value

    except Exception as e:
        print(f"EXIF 읽기 실패: {image_path}")
        print(e)

    return None


def organize_photos():
    image_extensions = (
        ".jpg",
        ".jpeg",
        ".png"
    )

    for filename in os.listdir(SOURCE_DIR):

        if not filename.lower().endswith(image_extensions):
            continue

        file_path = os.path.join(SOURCE_DIR, filename)

        photo_date = get_photo_date(file_path)

        if not photo_date:
            print(f"날짜 정보 없음: {filename}")
            continue

        try:
            dt = datetime.strptime(
                photo_date,
                "%Y:%m:%d %H:%M:%S"
            )

            folder_name = dt.strftime("%Y-%m-%d")

            target_dir = os.path.join(
                SOURCE_DIR,
                folder_name
            )

            os.makedirs(target_dir, exist_ok=True)

            target_path = os.path.join(
                target_dir,
                filename
            )

            shutil.move(
                file_path,
                target_path
            )

            print(
                f"{filename} -> {folder_name}"
            )

        except Exception as e:
            print(e)


if __name__ == "__main__":
    organize_photos()