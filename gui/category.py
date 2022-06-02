from distutils.util import execute
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
from turtle import clear
import customtkinter
import requests
import runpy
from api import api

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("light")

window = customtkinter.CTk()
window.geometry("1425x1000")
window.title("Manage Category - Smart Retail System")
window.eval('tk::PlaceWindow . center')
window.grid_columnconfigure(0, weight=1)


if not api.checkAuth():
    window.destroy()
    runpy.run_path(path_name='login.py')


def create():
    data = {'name': category.get()}
    response = requests.post(api.API_URL + 'categories', data = data, headers = {"Authorization": "Bearer " + api.getToken()})

    if not response.ok:
        messagebox.showerror(response.json()['status'], response.json()['message'])
        return
    
    messagebox.showinfo(response.json()['status'], response.json()['message'])
    refresh_tree()
    clear_text()
    return


def update():
    try:
        data = {'name': category.get()}
        id = str(tree.item(tree.selection()[0])['values'][0])
        response = requests.put(api.API_URL + 'categories/' + id, data = data, headers = {"Authorization": "Bearer " + api.getToken()})

        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message'])
            return
        
        messagebox.showinfo(response.json()['status'], response.json()['message'])
        refresh_tree()
        clear_text()
        return
    except IndexError:
        messagebox.showinfo('Info', 'Nothing To Update')
        return


def delete():
    try:
        id = str(tree.item(tree.selection()[0])['values'][0])
        response = requests.delete(api.API_URL + 'categories/' + id, headers = {"Authorization": "Bearer " + api.getToken()})

        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message'])
            return
        
        messagebox.showinfo(response.json()['status'], response.json()['message'])
        refresh_tree()
        clear_text()
        return
    except IndexError:
        messagebox.showinfo('Info', 'Nothing To Delete')
        return


def clear_text():
    category.delete(0, END)


def select_item(event):
    clear_text()

    try:
        item = tree.item(tree.selection()[0])['values']
        response = api.show('categories', str(item[0]));
        if response == False:
            return
        
        category.insert(0, response['name'] or '')
        tree.selection_clear()
    except IndexError:
        return

def refresh_tree():
    tree.delete(*tree.get_children())

    categories = api.list('categories')
    if categories == False:
        return

    for category in categories:
        tree.insert('', END, values=(category['id'],category['name'],category['user']['name']))
        tree.selection_clear()


# Menu Frame
menuFrame = customtkinter.CTkFrame(master=window, fg_color=window.cget('bg')) # Set Default Color of Window
menuFrame.grid(row=1, columnspan=2, sticky="nswe")

# Form Frame
formFrame = customtkinter.CTkFrame(master=window)
formFrame.grid(row=2, column=0, sticky="nswe", pady=(50,0))

# List Frame
listFrame = customtkinter.CTkFrame(master=window)
listFrame.grid(row=2, column=1, sticky="nswe", pady=(50,0))


################### Heading ##################
heading = customtkinter.CTkLabel(master=window,
                               textvariable=tkinter.StringVar(value="Manage Category"),
                               text_font=("", 50, "bold"))
heading.grid(row=0, columnspan=2, pady=15)
################### End of Heading ##################


################### Menu ##################
def manageOrderMenu():
    window.destroy()
    runpy.run_path(path_name='order.py')

manageOrderMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 text="Manage Order",
                                 text_font=("", 20, ""),
                                 command=manageOrderMenu)
manageOrderMenu.pack(side=tkinter.LEFT, padx=(0,30))

def viewOrderMenu():
    window.destroy()
    runpy.run_path(path_name='view.py')

viewOrderMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 text="View Order",
                                 text_font=("", 20, ""),
                                 command=viewOrderMenu)
viewOrderMenu.pack(side=tkinter.LEFT, padx=(0,30))

def customerMenu():
    window.destroy()
    runpy.run_path(path_name='customer.py')

customerMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 text="Customer",
                                 text_font=("", 20, ""),
                                 command=customerMenu)
customerMenu.pack(side=tkinter.LEFT, padx=(0,30))


categoryMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 fg_color='#00008B',
                                 text_color='white',
                                 text="Category",
                                 text_font=("", 20, ""))
categoryMenu.pack(side=tkinter.LEFT, padx=(0,30))

def productMenu():
    window.destroy()
    runpy.run_path(path_name='product.py')

productMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 text="Product",
                                 text_font=("", 20, ""),
                                 command=productMenu)
productMenu.pack(side=tkinter.LEFT, padx=(0,30))

def rfidMenu():
    window.destroy()
    runpy.run_path(path_name='rfid.py')

rfidMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 text="RFID",
                                 text_font=("", 20, ""),
                                 command=rfidMenu)
rfidMenu.pack(side=tkinter.LEFT, padx=(0,30))

def logout():
    window.destroy()
    api.setToken('')
    runpy.run_path(path_name='login.py')

logout = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 text="Logout",
                                 text_font=("", 20, ""),
                                 command=logout)
logout.pack(side=tkinter.RIGHT)
################### End of Menu ##################


################### From ##################
# Form Heading
formHeading = customtkinter.CTkLabel(master=formFrame,
                            textvariable=tkinter.StringVar(value="Create Category"),
                            text_font=("", 25, "bold"))
formHeading.pack(pady=(100, 30))

# Category Name
category = customtkinter.CTkEntry(master=formFrame,
                               placeholder_text="Category Name",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
category.pack(pady=(20,0))

# Add Button
addButton = customtkinter.CTkButton(master=formFrame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Create",
                                 text_font=("", 0, "bold"),
                                 command=create)
addButton.pack(pady=(20, 0))

# Update Delete Frame
updateDeleteFrame = customtkinter.CTkFrame(master=formFrame,
                               width=200,
                               height=200,
                               fg_color=None,
                               corner_radius=10)
updateDeleteFrame.pack(pady=(20, 0))

# Update Button
updateButton = customtkinter.CTkButton(master=updateDeleteFrame,
                                 width=190,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color='green',
                                 text_color='white',
                                 text="Update",
                                 text_font=("", 0, "bold"),
                                 command=update)
updateButton.pack(side=LEFT, padx=(0, 20))

# Delete Button
deleteButton = customtkinter.CTkButton(master=updateDeleteFrame,
                                 width=190,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color='#880808',
                                 text_color='white',
                                 text="Delete",
                                 text_font=("", 0, "bold"),
                                 command=delete)
deleteButton.pack(side=LEFT)
################### End of From ##################


################### Table #########################
columns = ('id', 'name', 'created_by')

tree = ttk.Treeview(listFrame, columns=columns, height=30, show='headings')

tree.heading('id', text='#')
tree.heading('name', text='Product Name')
tree.heading('created_by', text='Created By')

tree.pack()

refresh_tree()

tree.bind('<<TreeviewSelect>>', select_item)

################### End of Table ##################

window.mainloop()