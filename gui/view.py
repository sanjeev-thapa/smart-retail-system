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
window.title("View Order - Smart Retail System")
window.eval('tk::PlaceWindow . center')
window.grid_columnconfigure(0, weight=1)


if not api.checkAuth():
    window.destroy()
    runpy.run_path(path_name='login.py')


def select_item(event):
    subTree.delete(*subTree.get_children())

    for selected_item in tree.selection():
        item = tree.item(selected_item)['values']

        order = api.show('orders', str(item[0]))
        for orderItem in order['order_items']:
            subTree.insert("", END, value=(orderItem['rfid']['rfid'], orderItem['product']['name'],  orderItem['product']['category']['name'], orderItem['product']['price']))

def button_event():
    ""


# Menu Frame
menuFrame = customtkinter.CTkFrame(master=window, fg_color=window.cget('bg')) # Set Default Color of Window
menuFrame.grid(row=1, sticky="nswe")

# List Frame
listFrame = customtkinter.CTkFrame(master=window)
listFrame.grid(row=2, sticky="nswe", pady=(25,0))

# Sub List Frame
subListFrame = customtkinter.CTkFrame(master=window)
subListFrame.grid(row=3, sticky="nswe", pady=(25,0))


################### Heading ##################
heading = customtkinter.CTkLabel(master=window,
                               textvariable=tkinter.StringVar(value="View Order"),
                               text_font=("", 50, "bold"))
heading.grid(row=0, pady=15)
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

viewOrderMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 fg_color='#00008B',
                                 text_color='white',
                                 text="View Order",
                                 text_font=("", 20, ""))
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
                                 text_font=("", 20, ""),
                                 command=categoryMenu)
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

################### Table #########################
# List
listHeading = customtkinter.CTkLabel(master=listFrame,
                               textvariable=tkinter.StringVar(value="View Order"),
                               text_font=("", 25, "bold"))
listHeading.pack(pady=15)

columns = ('id', 'amount', 'payment_type', 'customer')

tree = ttk.Treeview(listFrame, columns=columns, show='headings')

tree.heading('id', text='#')
tree.heading('amount', text='Amount')
tree.heading('payment_type', text='Payment Type')
tree.heading('customer', text='Customer')

tree.pack()

orders = api.list('orders')
for order in orders:
    tree.insert('', END, values=(order['id'], order['amount'], order['payment_type'], order['customer']['name']))

tree.bind('<<TreeviewSelect>>', select_item)


# Sub List
listHeading = customtkinter.CTkLabel(master=subListFrame,
                               textvariable=tkinter.StringVar(value="View Order Items"),
                               text_font=("", 25, "bold"))
listHeading.pack(pady=15)
columns = ('rfid', 'product', 'category', 'price')

subTree = ttk.Treeview(subListFrame, columns=columns, show='headings')

subTree.heading('rfid', text='RFID')
subTree.heading('product', text='product')
subTree.heading('category', text='Product')
subTree.heading('price', text='Price')

subTree.pack()

################### End of Table ##################

window.mainloop()