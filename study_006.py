import math
print("-- 삼가함수 구하기 --")
degree = input(" 상수 입력 : ")

rad = math.pi * float(degree) /180.0

# 결과값 출력
print(" sin : ",math.sin(rad))
print(" cos : ",math.cos(rad))
print(" tan : ",math.tan(rad))