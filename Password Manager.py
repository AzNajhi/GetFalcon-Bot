# A simple script to calculate BMI
from pywebio.input import *
from pywebio.output import *
import pyrebase
import json

config = {
    'apiKey': "AIzaSyBi1ESfQtPqk7i-pbR_i5UkOVNUM49ESao",
    'authDomain': "password-manager-e6c57.firebaseapp.com",
    'databaseURL': "https://password-manager-e6c57-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "password-manager-e6c57",
    'storageBucket': "password-manager-e6c57.appspot.com",
    'messagingSenderId': "972053983045",
    'appId': "1:972053983045:web:a8fdf7e435f85fff71d82c"
    }
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def Register():
    username = input("Please register your Username：", type=TEXT, placeholder='Username', required=True)
    users = db.child("Users").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    password = input("Please register your Password：", type=PASSWORD, placeholder='Password',required=True)
    data = {'Password' : password}
    for (k, v) in users.items():
        if(str(k)!=str(username)):
            db.child("Users").child(username).set(data)
        else:
            with popup("Registration Error"):
                put_text("Sorry, the Username has been used!")

def Login():
    username = input("Username：", type=TEXT, required=True)
    password = input("Password：", type=PASSWORD, required=True)
    users = db.child("Users").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    print(users)
    for (k, v) in users.items():
        print(k)
        print(v)
        if(str(k)==str(username)):
            if(str(v["Password"])==str(password)):
                while True:
                    option = radio("Hello {}, What can I do for you?".format(username), options=['Add Account', 'View Account', 'Edit Account', 'Generate Password'])
                    if option == 'Add Account':
                        Add_Account()
                    elif option == 'View Account':
                        View_Account()
                    elif option == 'Edit Account':
                        Edit_Account()
                    elif option == 'Generate Password':
                        Gen_Pass()
            else:
                with popup("Login Error"):
                    put_text("Sorry, incorrect Username/Password!")

def Intro():
    while True:
        home = radio("Welcome to Password Manager", options=['Login', 'Register'])        
        if home == 'Login':
            Login()
        elif home == 'Register':
            Register()

if __name__ == '__main__':
    while True:
        intro()