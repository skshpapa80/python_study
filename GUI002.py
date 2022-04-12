from tkinter import *
from tkinter import messagebox

root = Tk()
# 윈도우 타이틀 지정
root.title("Windows Title")

#윈도우 사이즈 지정
root.geometry("640x480+100+100") # 가로 * 세로 + X좌표 + Y좌표

#윈도우 사이즈 조절 여부
root.resizable(False, False) # X(너비), Y(높이) 크기변경 불가

root.mainloop()  
