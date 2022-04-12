from tkinter import *
from tkinter import messagebox

class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

   

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("GUI Window")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # 버튼 인스턴스 생성
        quitButton = Button(self, text="Message", command=okClick)

        # placing the button on my window
        quitButton.place(x=0, y=0)

# 버튼 클릭 이벤트 핸들러
def okClick():
    messagebox.showinfo("메세지", "안녕하세요")    

root = Tk()

#윈도우 사이즈 지정
root.geometry("500x400")

app = Window(root)
root.mainloop()  
