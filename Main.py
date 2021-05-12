from tkinter import *
import sqlite3
import string
import random
import tkinter.messagebox as tkMessageBox

root = Tk()
root.geometry('500x500')
root.title("user Form")
 
width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

Fullname=StringVar()
Email=StringVar()
Phone_number = IntVar()



def database():
   name1=Fullname.get()
   email=Email.get()
   phone_number=Phone_number.get()
   number = '{:05d}'.format(random.randrange(1, 999))
   three_letters_name = name[-1][:3]
   username = (three_letters_name + number)
   password=id_generator()
   conn = sqlite3.connect('Form.db')
   
   with conn:
      cursor=conn.cursor()
   cursor.execute('CREATE TABLE IF NOT EXISTS User (Name TEXT,Email TEXT,Phone_number TEXT,Username TEXT,Password TEXT)')
   cursor.execute('INSERT INTO Student (Name,Email,Phone_number,Username,Password) VALUES(?,?,?,?,?)',(name1,email,phone_number,username,password,))
   conn.commit()
   
def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
   
def id_generator(size=6, chars= string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
    
def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)
   
   
def RegistrationForm():  
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    label_0 = Label(RegisterFrame, text="Registration form",width=20,font=("bold", 20))
    label_0.place(x=90,y=53)
    
    
    label_1 = Label(RegisterFrame, text="FullName",width=20,font=("bold", 10))
    label_1.place(x=80,y=130)
    
    entry_1 = Entry(RegisterFrame,textvar=Fullname)
    entry_1.place(x=240,y=130)
    
    label_2 = Label(RegisterFrame, text="Email",width=20,font=("bold", 10))
    label_2.place(x=68,y=180)
    
    entry_2 = Entry(RegisterFrame,textvar=Email)
    entry_2.place(x=240,y=180)
    
    label_3 = Label(RegisterFrame, text="Phone Number",width=20,font=("bold", 10))
    label_3.place(x=68,y=180)
    
    entry_3 = Entry(RegisterFrame,textvar=Phone_number)
    entry_3.place(x=240,y=180)
    
    
    btn_login = Button(RegisterFrame, text='Submit',width=20,bg='brown',fg='white',command=database).place(x=180,y=380)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")
LoginForm()

#========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()