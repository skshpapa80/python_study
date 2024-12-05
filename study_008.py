import PIL.Image

#이미지 포멧, 모드, 사이즈 가져오기
img = PIL.Image.open("이미지경로")

print('Image Format : ' + img.format)
print('Image mode : ' +img.mode)
print('Image Size(X,Y) : ', end='')
print(img.size)
