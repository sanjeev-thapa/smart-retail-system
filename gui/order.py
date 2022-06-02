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
window.title("Manage Order - Smart Retail System")
window.eval('tk::PlaceWindow . center')
window.grid_columnconfigure(0, weight=1)


if not api.checkAuth():
    window.destroy()
    runpy.run_path(path_name='login.py')


added_rfids = []
def add():
    response = api.show('rfids', rfid.get())

    if not response:
        return

    if response['is_paid'] == 'y':
        messagebox.showwarning('Warning', 'Already Paid')
        clear_text()
        return

    if response['rfid'] in added_rfids:
        messagebox.showwarning('Warning', 'Product with this RFID Already Added')
        clear_text()
        return

    try:
        int(quantity.get())
    except ValueError:
        messagebox.showwarning('Warning', 'Quantity Must be an Integer')
        return

    tree.insert('', END, values=(response['rfid'], response['product']['name'], response['product']['price'], quantity.get()))
    added_rfids.append(response['rfid'])
    clear_text()
    return True


def update():
    try:
        for selected_item in tree.selection():
            response = api.show('rfids', rfid.get())
            if not response:
                return
            
            item = tree.item(selected_item)['values']
            tree.delete(selected_item)
            added_rfids.remove(item[0])
            if add() != True:
                return
            clear_text()
            return
    except IndexError:
        messagebox.showinfo('Info', 'Nothing To Update')

def delete():
    if messagebox.askyesno('Error', 'Are you sure to delete ?'):
        try:
            rfid = tree.item(tree.selection()[0])['values'][0]
            if rfid in added_rfids:
                added_rfids.remove(rfid)
            tree.delete(tree.selection()[0])
        except IndexError:
            messagebox.showinfo('Info', 'Nothing To Delete')

def scan():
    response = api.getFromRFID()
    clear_text()
    if not response:
        return
    product.insert(0, response['product']['name'])
    rfid.insert(0, response['rfid'])
    quantity.insert(0, 1)

def create_order():
    children = []
    amount = 0

    if len(tree.get_children()) <= 0:
        messagebox.showerror('Error', 'No Order Items')
        return

    for child in tree.get_children():
        amount += float(tree.item(child)["values"][2]) * float(tree.item(child)["values"][3])

    # Create Order
    data = {
        'amount' : amount,
        'customer_id' : customer.get().split('-')[0]
    }
    response = requests.post(api.API_URL + 'orders', data=data, headers = {"Authorization": "Bearer " + api.getToken()});
    if not response.ok:
        messagebox.showerror(response.json()['status'], response.json()['message'])
        return

    # Fetch RFIDS from TreeList
    for child in tree.get_children():
        id = tree.item(child)["values"][0]

        response = requests.get(api.API_URL + 'rfids/' + id, headers = {"Authorization": "Bearer " + api.getToken()});
        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message'])
            return
        rfid = response.json()['message']

        # Create Order Items
        data = {
            'product_id' : rfid['product']['id'],
            'rfid' : rfid['rfid'],
            'order_id' : api.list('orders')[0]['id']
        }
        response = requests.post(api.API_URL + 'order-items', data=data, headers = {"Authorization": "Bearer " + api.getToken()});
        if not response.ok:
            messagebox.showerror(response.status_code, response.json()['message'])
            return
        
        # Update RFID Paid Status to True
        response = requests.put(api.API_URL + 'rfids/' + rfid['rfid'], data={'is_paid': 'y'}, headers = {"Authorization": "Bearer " + api.getToken()})
        if not response.ok:
            messagebox.showerror(response.status_code, response.json()['message'])
            return

    messagebox.showinfo(response.status_code, 'Order Created Successfully')
    tree.delete(*tree.get_children())
    customer.set("Select Customer")
    return


def clear_text():
    product.delete(0, END)
    rfid.delete(0, END)
    quantity.delete(0, END)

def customers():
    customers = []
    for customer in api.list('customers'):
        customers.append(f"{customer['id']}-{customer['name']}")
    return customers

def select_item(event):
    clear_text()
    for selected_item in tree.selection():
        item = tree.item(selected_item)['values']

        rfid.insert(0, item[0])
        product.insert(0, item[1])
        quantity.insert(0, item[3])


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
                               textvariable=tkinter.StringVar(value="Manage Order"),
                               text_font=("", 50, "bold"))
heading.grid(row=0, columnspan=2, pady=15)
################### End of Heading ##################


################### Menu ##################
manageOrderMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 fg_color='#00008B',
                                 text_color='white',
                                 text="Manage Order",
                                 text_font=("", 20, ""))
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


################### From ##################
#Scan
button = customtkinter.CTkButton(master=formFrame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Scan",
                                 text_font=("", 0, "bold"),
                                 command=scan)
button.pack(pady=20)

# RFID
rfid = customtkinter.CTkEntry(master=formFrame,
                               placeholder_text="RFID",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
rfid.pack(pady=(20,0))

# Product Name
product = customtkinter.CTkEntry(master=formFrame,
                               placeholder_text="Product Name",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
product.pack(pady=(20,0))

# Quantity
quantity = customtkinter.CTkEntry(master=formFrame,
                               placeholder_text="Quantity",
                               width=400,
                               height=50,
                               border_width=2,
                               corner_radius=10)
quantity.pack(pady=(20,0))


# Add Button
addButton = customtkinter.CTkButton(master=formFrame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Add",
                                 text_font=("", 0, "bold"),
                                 command=add)
addButton.pack(pady=20)

# Update Button
updateButton = customtkinter.CTkButton(master=formFrame,
                                 width=190,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color='green',
                                 text_color='white',
                                 text="Update",
                                 text_font=("", 0, "bold"),
                                 command=update)
updateButton.pack(side=tkinter.LEFT, padx=(110,0), pady=(0,20))

# Delete Button
deleteButton = customtkinter.CTkButton(master=formFrame,
                                 width=190,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 fg_color='#880808',
                                 text_color='white',
                                 text="Delete",
                                 text_font=("", 0, "bold"),
                                 command=delete)
deleteButton.pack(side=tkinter.LEFT, padx=(20,0), pady=(0,20))
################### End of From ##################


################### Table #########################
columns = ('rfid', 'product', 'price', 'quantity')

tree = ttk.Treeview(listFrame, columns=columns, show='headings')

tree.heading('rfid', text='rfid')
tree.heading('product', text='product')
tree.heading('price', text='price')
tree.heading('quantity', text='quantity')

tree.pack()

# Customer
customer = customtkinter.CTkOptionMenu(master=listFrame,
                                        width=400,
                                        height=50,
                                        fg_color=window.cget('bg'),
                                        button_color=window.cget('bg'),
                                        button_hover_color=window.cget('bg'),
                                        dropdown_color=window.cget('bg'),
                                        dropdown_hover_color="grey",
                                        dropdown_text_color='black',
                                        values=customers())
customer.set("Select Customer")
customer.pack(pady=20)

# Create Order Button
createOrder = customtkinter.CTkButton(master=listFrame,
                                 width=400,
                                 height=50,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Create Order",
                                 text_font=("", 0, "bold"),
                                 command=create_order)
createOrder.pack(pady=5)

tree.bind('<<TreeviewSelect>>', select_item)

################### End of Table ##################

window.mainloop()