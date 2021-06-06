from pywebio.input import *
from pywebio.output import *
import pyrebase
import random
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
            with popup("Message:"):
                put_text("Successfully created password manager account!")
        else:
            with popup("Registration Error:"):
                put_text("Sorry, the Username has been used!")

def Login():
    username = input("Username：", type=TEXT, required=True)
    password = input("Password：", type=PASSWORD, required=True)
    users = db.child("Users").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(k)==str(username)):
            if(str(v["Password"])==str(password)):
                while True:
                    option = radio("Hello {}, What can I do for you?".format(username), options=['Add Account', 'View Account', 'Edit Account', 'Generate Password'])
                    if option == 'Add Account':
                        Add_Account(username)
                    elif option == 'View Account':
                        View_Account(username)
                    elif option == 'Edit Account':
                        Edit_Account(username)
                    elif option == 'Generate Password':
                        Gen_Pass()
            else:
                with popup("Login Error:"):
                    put_text("Sorry, incorrect Username/Password!")

def Add_Account(name):
    account = input("Please enter an account：", type=TEXT, placeholder='Ex, Facebook or Google or Discord',required=True)
    username = input("Please enter the account's Email/Username：", type=TEXT, placeholder='Ex, User@gmail.com or User123',required=True)
    password = input("Please enter the account's Password：", type=PASSWORD, placeholder='Ex, Password123',required=True)
    data = {'Username': username, 'Password': password}
    users = db.child("Users").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(k)==str(name)):
            same = []
            for (key, value) in v.items():
                if(str(key)==str(account)):
                    same.append(key)
            count = len(same)
            if count == 0:
                db.child("Users").child(name).child(account).set(data)
                with popup("Message:"):
                    put_text("Successfully stored your account's info!")
            else:
                with popup("Error:"):
                    put_text("Sorry, that account's name has already been added!")

def View_Account(name):
    users = db.child("Users").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(k)==str(name)):
            accounts = []
            for (key, value) in v.items():
                    accounts.append(key)
    accounts.remove('Password')
    if len(accounts) == 0:
        with popup("Message:"):
            put_text("Sorry, you have not added any account yet!")
        return
    option = radio("Please select an account that you want to view.", options=accounts)
    for (k, v) in users.items():        
        if(str(k)==str(name)):
            for (key, value) in v.items():                
                if(str(key)==str(option)):
                    username = value["Username"]
                    password = value["Password"]
                    with popup("Message:"):
                        put_text("{} Account:\nUsername: {}\nPassword: {}".format(option, username, password))

def Edit_Account(name):
    users = db.child("Users").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(k)==str(name)):
            accounts = []
            for (key, value) in v.items():
                    accounts.append(key)
    accounts.remove('Password')
    if len(accounts) == 0:
        with popup("Message:"):
            put_text("Sorry, you have not added any account yet!")
        return
    option = radio("Please select an account that you want to edit.", options=accounts)
    user_or_pass = radio("Please choose what you want to edit.", options=['Username','Password'])
    if user_or_pass == 'Username':
        username = input("Please enter new Username：", type=TEXT, placeholder='New Username',required=True)
        data = {'Username' : username}
        db.child("Users").child(name).child(option).update(data)
        with popup("Message:"):
            put_text("Username successfully changed!")
    if user_or_pass == 'Password':
        password = input("Please enter new Password：", type=TEXT, placeholder='New Password',required=True)
        data = {'Password' : password}
        db.child("Users").child(name).child(option).update(data)
        with popup("Message:"):
            put_text("Password successfully changed!")

def Gen_Pass():
    all = ''
    upper_case = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_case = 'abcdefghijklmnopqrstuvwxyz'
    digit = '0123456789'
    symbol = '()[]{}<>~!@#$%^&*-=_+?.,;/'
    upper, lower, num, symb = False, False, False, False
    choices = checkbox("Please select what you want to include in your password", options=['Upper Case', 'Lower Case', 'Number', 'Symbol'])
    
    for x in choices:
        if x == 'Upper Case':
            upper = True
        elif x == 'Lower Case':
            lower = True
        elif x == 'Number':
            num = True
        elif x == 'Symbol':
            symb = True
    
    if upper:
        all += upper_case
    if lower:
        all += lower_case
    if num:
        all += digit
    if symb:
        all += symbol
    
    length = 15
    password = "".join(random.sample(all, length))
    with popup("Random Password:"):
        put_text(password)

def Intro():
    while True:
        home = radio("Welcome to Password Manager", options=['Login', 'Register'])
        if home == 'Login':
            Login()
        elif home == 'Register':
            Register()

if __name__ == '__main__':
    while True:
        Intro()
