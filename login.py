from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
#Login Function
def Login():
    if Username_field.get() == "" or Password_field.get() == "":
        messagebox.showerror("error","Fields cannot be empty")
    elif Username_field.get() == "admin" and Password_field.get() == "csc":
        # messagebox.showinfo("Success","Logged in") //can be inserted if you want to display a success message.
        window.destroy()
        import main  
    else:
        messagebox.showerror("error","Invalid Username and Password")


window = Tk()
window.geometry("1500x700+0+0")
window.title("Student Management System")
#background
bgImage = ImageTk.PhotoImage(file="bg.jpg")
bgLabel = Label(window,image=bgImage)
#Login frame
LoginFrame = Frame(window,height=450,width=450,bg="#eeeee4")
LoginFrame.place(x=500,y=130)
#Logo Image
Logo = PhotoImage(file="Login.png")
LogoLabel = Label(LoginFrame,image=Logo)
LogoLabel.place(x=150,y=20)
#Username Label
Username = Label(LoginFrame,text="Username :",font=("arial",15),bg="#eeeee4")
Username.place(x=50,y=200)
Username_field = Entry(LoginFrame, font=("arial",15))
Username_field.place(x=170, y=200)
#password label
Password = Label(LoginFrame,text="Password :",font=("arial",15),bg="#eeeee4")
Password.place(x=50,y=250)
Password_field = Entry(LoginFrame,font=("arial",15))
Password_field.place(x=170,y=250)
#Login Button
LoginButton = Button(LoginFrame,text="Login",font=("arial",15),bg="cornflowerblue",fg="white",cursor="hand2",
                activebackground="cornflowerblue",height=1,width=15,command=Login)
LoginButton.place(x=140,y=330)

bgLabel.place(x=2,y=0)
window.mainloop()