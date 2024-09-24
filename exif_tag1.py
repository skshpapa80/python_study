import PIL.Image
from PIL.ExifTags import TAGS

# 이미지 정보 읽어 오기
img1 = PIL.Image.open("이미지경로")
meta_data = img1.getexif()

# 새로운 딕셔너리 생성
taglabel = {}

for tag, value in meta_data.items():
    decoded = TAGS.get(tag, tag)
    taglabel[decoded] = value

# exif 정보 출력
print(taglabel)

print(img1.width, img1.height)

