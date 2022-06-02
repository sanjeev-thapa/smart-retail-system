from urllib import request
import requests
from tkinter import messagebox
import runpy

API_URL = "http://localhost:8000/v1/"
python = "python3"

class api:

    API_URL = API_URL
    python = python

    # Login
    def login(username, password):
        response = requests.post(API_URL + 'login', {
            'username': username,
            'password': password
        })
        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message']);
            return False
        api.setToken(response.json()['message']['access_token'])
        return True

    # RFID Login
    def rfidLogin():
        response = requests.post(API_URL + 'rfid-login')
        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message']);
            return False
        api.setToken(response.json()['message']['access_token'])
        return True
    
    # Set Token
    def setToken(token):
        f = open("token", "w")
        f.write(token)
        f.close()
    
    # Set Token
    def getToken():
        try:
            f = open("token", "r")
            return f.read()
        except FileNotFoundError:
            return ""
    
    def checkAuth():
        headers = {"Authorization": "Bearer " + api.getToken()}
        response = requests.get(API_URL + 'me', headers=headers)
        if response.status_code == 401:
            return False;
        return True;
    
    # List
    def list(resource):
        headers = {"Authorization": "Bearer " + api.getToken()}
        response = requests.get(API_URL + resource, headers=headers)
        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message']);
            return False
        return response.json()['message']['data']

    def show(resource, id):
        headers = {"Authorization": "Bearer " + api.getToken()}
        response = requests.get(API_URL + resource + '/' + id, headers=headers)
        if not response.ok:
            messagebox.showerror(response.json()['status'], response.json()['message']);
            return False
        return response.json()['message']
    
    # Scan
    def getFromRFID():
        response = requests.get(API_URL + 'arduino/get');
        if not response.ok:
            messagebox.showerror(response.json()['status'], 'RFID Not Found. Please Try Again');
            return False
        return response.json()['message']

