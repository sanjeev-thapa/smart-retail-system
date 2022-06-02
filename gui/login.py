import tkinter
import customtkinter
import runpy
from api import api


customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("light")

window = customtkinter.CTk()
window.geometry("500x550")
window.title("Login - Smart Retail System")
window.eval('tk::PlaceWindow . center')

def login():
    if api.login(username.get(), password.get()):
        window.destroy()
        runpy.run_path(path_name='order.py')

def rfid_login():
    if api.rfidLogin():
        window.destroy()
        runpy.run_path(path_name='order.py')

# Frame
frame = customtkinter.CTkFrame(master=window)
frame.pack(pady=25, padx=25, fill="both", expand=True)



label = customtkinter.CTkLabel(master=frame,
                               textvariable=tkinter.StringVar(value="Login"),
                               text_font=("", 50, "bold"))
label.pack(padx=20, pady=(50,0))

# Username
username = customtkinter.CTkEntry(master=frame,
                               placeholder_text="Username",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
username.pack(padx=20, pady=(50,0))

# Password
password = customtkinter.CTkEntry(master=frame,
                               placeholder_text="Password",
                               show="*",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
password.pack(padx=20, pady=(20,0))

# Login Button
loginButton = customtkinter.CTkButton(master=frame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Login",
                                 text_font=("", 0, "bold"),
                                 command=login)
loginButton.pack(padx=20, pady=(20,0))

# RFID Login Button
rfidLoginButton = customtkinter.CTkButton(master=frame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Login from RFID Card",
                                 text_font=("", 0, "bold"),
                                 command=rfid_login)
rfidLoginButton.pack(padx=20, pady=(20,0))

window.mainloop()