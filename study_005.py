import math
print("-- 원 면적 계산 프로그램 --")
r = input(" 반지름 입력 : ")
cal = math.pi*float(r)*float(r);    #r*r==r**2
print("반지름 : ",r,", 원면적 : ",cal)