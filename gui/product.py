from distutils.util import execute
from email import message
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
window.title("Manage Products - Smart Retail System")
window.eval('tk::PlaceWindow . center')
window.grid_columnconfigure(0, weight=1)


if not api.checkAuth():
    window.destroy()
    runpy.run_path(path_name='login.py')


def create():
    data = {
        'name': name.get(),
        'price': price.get(),
        'category_id': category.get().split('-')[0] or 0
    }
    response = requests.post(api.API_URL + 'products', data = data, headers = {"Authorization": "Bearer " + api.getToken()})

    if not response.ok:
        messagebox.showerror(response.json()['status'], response.json()['message'])
        return
    
    messagebox.showinfo(response.json()['status'], response.json()['message'])
    refresh_tree()
    toplevel.destroy()
    return


def update():
    try:
        data = {
            'name': name.get(),
            'price': price.get(),
            'category_id': category.get().split('-')[0] or 0
        }
        id = str(tree.item(tree.selection()[0])['values'][0])
        response = requests.put(api.API_URL + 'products/' + id, data = data, headers = {"Authorization": "Bearer " + api.getToken()})

        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message'])
            return
        
        messagebox.showinfo(response.json()['status'], response.json()['message'])
        refresh_tree()
        toplevel.destroy()
        return
    except IndexError:
        messagebox.showinfo('Info', 'Nothing To Update')
        return

def delete():
    try:
        id = str(tree.item(tree.selection()[0])['values'][0])
        response = requests.delete(api.API_URL + 'products/' + id, headers = {"Authorization": "Bearer " + api.getToken()})

        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message'])
            return
        
        messagebox.showinfo(response.json()['status'], response.json()['message'])
        refresh_tree()
        toplevel.destroy()
        return
    except IndexError:
        messagebox.showinfo('Info', 'Nothing To Delete')
        return


def clear_text():
    name.delete(0, END)
    price.delete(0, END)
    category.set(0)


def refresh_tree():
    tree.delete(*tree.get_children())
    response = api.list('products')
    if response == False:
        return
    for item in response:
        tree.insert('', END, values=(item['id'],item['name'],item['price'],item['category']['name'],item['user']['name']))
        tree.selection_clear()


def select_item(event):
    create_toplevel('update')
    clear_text()

    try:
        item = tree.item(tree.selection()[0])['values']
        response = api.show('products', str(item[0]));
        if response == False:
            return
        
        name.insert(0, response['name'] or '')
        price.insert(0, response['price'] or '')
        category.set(f"{response['category']['id']}-{response['category']['name']}" or '')
        tree.selection_clear()
    except IndexError:
        toplevel.destroy()
        return

def categories():
    categories = []
    response = api.list('categories')
    if response == False:
        return ()
    for category in response:
        categories.append(f"{category['id']}-{category['name']}")
    return tuple(categories)


def create_toplevel(type = 'create'):
    global toplevel
    toplevel = customtkinter.CTkToplevel(window)
    toplevel.title('Create Customer' if type == "create" else "Edit Customer")
    toplevel.geometry("625x625")

    ################### From ##################
    # Form Heading
    formHeading = customtkinter.CTkLabel(master=toplevel,
                               textvariable=tkinter.StringVar(value="Create Customer" if type == "create" else "Edit Customer"),
                               text_font=("", 25, "bold"))
    formHeading.pack(pady=15)

    # Product Name
    global name
    name = customtkinter.CTkEntry(master=toplevel,
                                placeholder_text="Name*",
                                width=400,
                                height=50,
                                border_width=2,
                                corner_radius=10)
    name.pack(pady=(20,0))

    # Price
    global price
    price = customtkinter.CTkEntry(master=toplevel,
                                placeholder_text="Price",
                                width=400,
                                height=50,
                                border_width=2,
                                corner_radius=10)
    price.pack(pady=(20,0))

    # Category
    global category
    category = customtkinter.CTkOptionMenu(master=toplevel,
                                            width=400,
                                            height=50,
                                            fg_color='white',
                                            button_color='white',
                                            button_hover_color='white',
                                            dropdown_color='white',
                                            dropdown_hover_color="grey",
                                            dropdown_text_color='black',
                                            values=categories())
    category.pack(pady=20)

    if type == 'create':
        # Create Button
        createButton = customtkinter.CTkButton(master=toplevel,
                                        width=400,
                                        height=50,
                                        border_width=0,
                                        corner_radius=8,
                                        text="Add",
                                        text_font=("", 0, "bold"),
                                        command=create)
        createButton.pack(pady=(20, 0))
    else :
        # Update Button
        updateButton = customtkinter.CTkButton(master=toplevel,
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
        deleteButton = customtkinter.CTkButton(master=toplevel,
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


# Menu Frame
menuFrame = customtkinter.CTkFrame(master=window, fg_color=window.cget('bg')) # Set Default Color of Window
menuFrame.grid(row=1, columnspan=2, sticky="nswe")

# List Frame
listFrame = customtkinter.CTkFrame(master=window)
listFrame.grid(row=3, columnspan=2, sticky="nswe", pady=(50,0))


################### Heading ##################
heading = customtkinter.CTkLabel(master=window,
                               textvariable=tkinter.StringVar(value="Manage Customer"),
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
                                 text="Manage Customer",
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
                                 text_font=("", 20, ""),
                                 command=categoryMenu)
categoryMenu.pack(side=tkinter.LEFT, padx=(0,30))


productMenu = customtkinter.CTkButton(master=menuFrame,
                                 width=150,
                                 height=50,
                                 border_width=0,
                                 corner_radius=0,
                                 fg_color='#00008B',
                                 text_color='white',
                                 text="Product",
                                 text_font=("", 20, ""))
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
topListFrame = customtkinter.CTkFrame(master=listFrame,
                               width=1000,
                               height=200,
                               fg_color=None)
topListFrame.pack(pady=20, side=TOP)

listHeading = customtkinter.CTkLabel(master=topListFrame,
                               textvariable=tkinter.StringVar(value="Products"),
                               text_font=("", 25, "bold"))
listHeading.pack(side=LEFT, padx=(0,100))

button = customtkinter.CTkButton(topListFrame, text="Create Products", height=40, command=create_toplevel)
button.pack(side=RIGHT)

columns = ('id', 'name', 'price', 'category', 'created_by')

tree = ttk.Treeview(listFrame, columns=columns, show='headings', height=25)

tree.heading('id', text='#')
tree.heading('name', text='Name')
tree.heading('price', text='Price')
tree.heading('category', text='Category')
tree.heading('created_by', text='Created By')

tree.pack(side=BOTTOM, anchor=S)

refresh_tree()

tree.bind('<<TreeviewSelect>>', select_item)

################### End of Table ##################

window.mainloop()