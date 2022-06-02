from distutils.util import execute
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter
import customtkinter
import requests
import runpy
from api import api

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("light")

window = customtkinter.CTk()
window.geometry("1425x1000")
window.title("Link RFID - Smart Retail System")
window.eval('tk::PlaceWindow . center')
window.grid_columnconfigure(0, weight=1)


if not api.checkAuth():
    window.destroy()
    runpy.run_path(path_name='login.py')


def create():
    data = {
        'rfid': rfid.get(),
        'is_paid': 'n',
        'product_id': product.get().split('-')[0] or '0'
    }
    response = requests.post(api.API_URL + 'rfids', data = data, headers = {"Authorization": "Bearer " + api.getToken()})

    if not response.ok:
        messagebox.showerror(response.json()['status'], response.json()['message'])
        return
    
    messagebox.showinfo(response.json()['status'], response.json()['message'])
    refresh_tree()
    clear_text()
    return


def update():
    try:
        data = {
            'rfid': rfid.get(),
            'product_id': product.get().split('-')[0] or 0
        }
        id = str(tree.item(tree.selection()[0])['values'][0])
        response = requests.put(api.API_URL + 'rfids/' + id, data = data, headers = {"Authorization": "Bearer " + api.getToken()})

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
        response = requests.delete(api.API_URL + 'rfids/' + id, headers = {"Authorization": "Bearer " + api.getToken()})

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
    rfid.delete(0, END)
    product.set('0-Select Product')


def select_item(event):
    clear_text()

    try:
        item = tree.item(tree.selection()[0])['values']
        response = api.show('rfids', str(item[0]));
        if response == False:
            return
        
        rfid.insert(0, response['rfid'] or '')
        product.set(f"{response['product']['id']}-{response['product']['name']}" or 0)
        tree.selection_clear()
    except IndexError:
        return

def refresh_tree():
    tree.delete(*tree.get_children())

    rfids = api.list('rfids')
    if rfids == False:
        return

    for rfid in rfids:
        paid_status = 'Paid' if rfid['is_paid'] == 'y' else 'Not Paid'
        tree.insert('', END, values=(rfid['rfid'],paid_status,rfid['product']['name'],rfid['product']['category']['name'],rfid['linked_date']))
        tree.selection_clear()


def products():
    products = []
    response = api.list('products')
    if response == False:
        return ()
    for product in response:
        products.append(f"{product['id']}-{product['name']}")
    return tuple(products)


def scan():
    response = requests.get('http://localhost:8000/v1/arduino/scan')
    if not response.ok:
        messagebox.showerror('error', 'An Error Occurred')
        return
    if response == "":
        messagebox.showerror('error', 'RFID Not Found')
        return
    rfid.delete(0, END)
    rfid.insert(0, response.text)


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
                               textvariable=tkinter.StringVar(value="Link RFID"),
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


def categoryMenu():
    window.destroy()
    runpy.run_path(path_name='category.py')

categoryMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
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


rfidMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 fg_color='#00008B',
                                 text_color='white',
                                 text="RFID",
                                 text_font=("", 20, ""))
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
                            textvariable=tkinter.StringVar(value="Link RFID"),
                            text_font=("", 25, "bold"))
formHeading.pack(pady=(80, 30))

# Scan Button
scanButton = customtkinter.CTkButton(master=formFrame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Scan",
                                 text_font=("", 0, "bold"),
                                 command=scan)
scanButton.pack(pady=(20, 0))

# RFID
rfid = customtkinter.CTkEntry(master=formFrame,
                               placeholder_text="RFID",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
rfid.pack(pady=(20,0))

# Product
product = customtkinter.CTkOptionMenu(master=formFrame,
                                        width=400,
                                        height=50,
                                        fg_color='white',
                                        button_color='white',
                                        button_hover_color='white',
                                        dropdown_color='white',
                                        dropdown_hover_color="grey",
                                        dropdown_text_color='black',
                                        values=products())
product.pack(pady=20)

# Add Button
addButton = customtkinter.CTkButton(master=formFrame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Link",
                                 text_font=("", 0, "bold"),
                                 command=create)
addButton.pack()

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
columns = ('rfid', 'is_paid', 'product', 'category', 'linked_date')

tree = ttk.Treeview(listFrame, columns=columns, height=30, show='headings')

tree.heading('rfid', text='RFID')
tree.heading('is_paid', text='Status')
tree.heading('product', text='Product')
tree.heading('category', text='Category')
tree.heading('linked_date', text='Linked Date')

tree.pack()

refresh_tree()

tree.bind('<<TreeviewSelect>>', select_item)

################### End of Table ##################

window.mainloop()