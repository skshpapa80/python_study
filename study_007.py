print("-- BMI 계산기 --")

num1 = input("키를 입력하세요. : ")
num2 = input("몸무개를 입력하세요. : ")

key = int(num1) / 100 #m 환산된 키
weight = int(num2) #몸무개

key = key * key #bmi 식 의 키
bmi = weight / key

# bmi 결과 
if bmi <= 18.5:
  result = '저체중'
elif bmi > 18.5 and bmi <= 23:
  result = '정상'
elif bmi > 23 and bmi <= 25:
  result = '과체중'
elif bmi > 25 and bmi <= 30:
  result ='경도비만'
else:
  result = '중등비만'

# bmi 결과 출력
print("-- BMI 결과 :", result)
