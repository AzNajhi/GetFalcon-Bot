import json
import logging
import pyrebase
import requests as requests
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,    
)
import os
PORT = int(os.environ.get('PORT', 5000))

config = {
  "apiKey" : "INSERT YOURS HERE",
  "authDomain" : "INSERT YOURS HERE",
  "databaseURL" : "INSERT YOURS HERE",
  "projectId" : "INSERT YOURS HERE",
  "storageBucket" : "INSERT YOURS HERE",
  "messagingSenderId" : "INSERT YOURS HERE",
  "appId" : "INSERT YOURS HERE"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
BEFORE_REG, CHECKCODE_REG, GETINFO_REG, NAME_REG, TYPE_REG, LOCATION_REG, CONFIRM_REG, GETSERVICEBEFORE, GETLOCATIONBEFORE, GETSERVICEBEF, GETLOCATIONBEF, GETMESSAGEBEF, TAKEN_BEFORE, FEED_BEF, AFTER_REG, GETINFO_CHANGE, CHANGENAME, CHANGETYPE, CHANGELOCATION, GETSERVICEAFTER, GETLOCATIONAFTER, GETSERVICEAFT, GETLOCATIONAFT, GETMESSAGEAFT, TAKEN_AFTER, UPDATESTATUS, FEED_AFT = range(27)

#============================================================KEYBOARD==========================================================================#

back = [
    ['Back']
]

after_reg = [
    ['View Information'],
    ['Change Information'],
    ['Update Status'],
    ['Get List'],
    ['Send a Request'],
    ['Give Feedback'],
    ['Exit']
]

features = [
    ['Get List'],
    ['Send a Request'],
    ['Give Feedback'],
    ['Register <for service providers>'],
    ['Exit']
]

update_info = [
    ['Name'],
    ['Service Type'],
    ['Location'],
    ['Back', 'Exit']
]

get_info_cancel = [
    ['Name'],
    ['Service Type'],
    ['Location'],
    ['Cancel', 'Exit']
]

get_info_with_confirm = [
    ['Name'],
    ['Service Type'],
    ['Location'],
    ['Cancel','Confirm']
]

service = [
    ['Runner'],
    ['Transporter']       
]

getservice = [
    ['Runner'],
    ['Transporter'],
    ['Back', 'Exit']
]

getlocation = [
    ['IIUM Gombak'],
    ['IIUM Kuantan'],
    ['IIUM Gambang'],
    ['IIUM Pagoh'],
]

updatestatus = [
    ['Check-in', 'Check-out'],
    ['Back', 'Exit']
]

taken = [
    ['Taken']
]

taken = ReplyKeyboardMarkup(taken, one_time_keyboard=True)
back = ReplyKeyboardMarkup(back, one_time_keyboard=True)
features = ReplyKeyboardMarkup(features, one_time_keyboard=True)
update_info = ReplyKeyboardMarkup(update_info, one_time_keyboard=True)
get_info_cancel = ReplyKeyboardMarkup(get_info_cancel, one_time_keyboard=True)
get_info_with_confirm = ReplyKeyboardMarkup(get_info_with_confirm, one_time_keyboard=True)
after_reg = ReplyKeyboardMarkup(after_reg, one_time_keyboard=True)
service = ReplyKeyboardMarkup(service, one_time_keyboard=True)
getservice = ReplyKeyboardMarkup(getservice, one_time_keyboard=True)
getlocation = ReplyKeyboardMarkup(getlocation, one_time_keyboard=True)
updatestatus = ReplyKeyboardMarkup(updatestatus, one_time_keyboard=True)

#=============================================================START============================================================================#
def start(update: Update, context: CallbackContext) -> int: 
    id = str(update.message.chat['id'])
    username = str(update.message.chat['username'])
    context.user_data['Username'] = username
    username = context.user_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(k)==str(id)):
            db.child("Employee").child(id).update(username)
            update.message.reply_text(
                "Hello {}, Welcome back! what can I do for you?".format(str(v["Name"])) +
                "\n\nIf you need any help on how to use this bot, please read our guidelines here @GetFalcon",                
                reply_markup=after_reg,
            )            
            return AFTER_REG
    update.message.reply_text(
        "Hi! I'm GetFalcon Bot. I'm here to provide a platform for you to get the list of your chosen services that are currently available. What can I do for you?" +
        "\n\nIf you need any help on how to use this bot, please read our guidelines here @GetFalcon" +
        "\n\nNOTICE: Currently, we're in a phase of testing this bot. If you are invited here to test this bot, feel free to do so." +
        "\n\nPlease use all the features available, including Register. The verification code to register is '000'." +
        "\n\nOnce you are done, please use the command 'Give Feedback', and type in your review in english. We will always try to improve this bot." +
        "\n\nLater on, we'll delete all available registered accounts and inform all registered members when the bot is released. Thank You. :)",
        reply_markup=features,
    )
    return BEFORE_REG

#=========================================================BEFORE REGISTER======================================================================#
#==========================================================REGISTRATION========================================================================#
def verification(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Please enter the verification code that we have sent to you to proceed:",
        reply_markup=back,
    )
    return CHECKCODE_REG
def checkcode(update: Update, context: CallbackContext) -> int:
    user_code = update.message.text
    verify_code = db.child("Verification Code").get()
    verify_code = verify_code.val()
    verify_code = json.dumps(verify_code, indent=2)
    verify_code = json.loads(verify_code)
    for (k, v) in verify_code.items():
        if(str(k)==str(user_code)):
            context.user_data['Name'] = ''
            context.user_data['Username'] = ''
            context.user_data['Type'] = ''
            context.user_data['Location'] = ''
            update.message.reply_text(
                "Your verification code is valid. You can now proceed with the registration."
            )
            update.message.reply_text(
                "Please fill in the information below:" +
                "\n\nName:" +
                "\nService Type:" +
                "\nLocation:",
                reply_markup=get_info_cancel,
            )
            return GETINFO_REG
    update.message.reply_text(
        "Sorry, the code you entered was invalid!"
    )
    update.message.reply_text(
        "Is there anything else I can help you with?",        
        reply_markup=features,
    )
    return BEFORE_REG
def name(update: Update, context: CallbackContext) -> int:
    context.user_data['Name']= ''
    update.message.reply_text(
        "Please enter your Name:"
    )
    return NAME_REG
def service_type(update: Update, context: CallbackContext) -> int:
    context.user_data['Type']= ''    
    update.message.reply_text(
        'Please choose the Service Type that you want to provide.',        
        reply_markup=service,
    )
    return TYPE_REG
def location(update: Update, context: CallbackContext) -> int:
    context.user_data['Location']= ''    
    update.message.reply_text(
        'Please choose the Location of your service.',        
        reply_markup=getlocation,
    )
    return LOCATION_REG
def enter_name(update: Update, context: CallbackContext) -> int:
    name = update.message.text
    context.user_data['Name'] = name
    user_data=context.user_data
    update.message.reply_text(
        "This is what you already filled in:" +
        "\n\nName: {}".format(user_data['Name']) +
        "\nService Type: {}".format(user_data['Type']) +
        "\nLocation: {}".format(user_data['Location']) +
        "\n\nPress 'Confirm' once you have filled all the required information.",
        reply_markup=get_info_with_confirm,
    )
    return CONFIRM_REG
def enter_type(update: Update, context: CallbackContext) -> int:
    type = update.message.text
    context.user_data['Type'] = type
    user_data=context.user_data
    update.message.reply_text(
        "This is what you have filled in:" +
        "\n\nName: {}".format(user_data['Name']) +
        "\nService Type: {}".format(user_data['Type']) +
        "\nLocation: {}".format(user_data['Location']) +
        "\n\nPress 'Confirm' once you have filled all the required information.",
        reply_markup=get_info_with_confirm,
    )
    return CONFIRM_REG
def enter_location(update: Update, context: CallbackContext) -> int:
    type = update.message.text
    context.user_data['Location'] = type
    user_data=context.user_data
    update.message.reply_text(
        "This is what you have filled in:" +
        "\n\nName: {}".format(user_data['Name']) +
        "\nService Type: {}".format(user_data['Type']) +
        "\nLocation: {}".format(user_data['Location']) +
        "\n\nPress 'Confirm' once you have filled all the required information.",
        reply_markup=get_info_with_confirm,
    )
    return CONFIRM_REG
def confirms(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    context.user_data['Username'] = str(update.message.chat['username'])
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(k)!=str(id)):
            context.user_data['Status']= 'Check-out'
            user_data = context.user_data
            id = str(update.message.chat['id'])
            db.child("Employee").child(id).set(user_data)
            update.message.reply_text(
                "Congratulation, You have successfully registered as our members!"
            )
            update.message.reply_text(
                "You have exited. All commands have been disabled.\n\nPlease use the /start command to start a new conversation with our bot."
            )
            user_data.clear()
            return ConversationHandler.END

#============================================================GET LIST==========================================================================#
def getservice_before(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "What kind of services that you are searching for?",             
        reply_markup=getservice,
    )
    return GETSERVICEBEFORE
def getlocation_before(update: Update, context: CallbackContext) -> int:
    service = update.message.text
    context.chat_data['Type'] = service            
    update.message.reply_text(
        "Please select a location of your selected service:",        
        reply_markup=getlocation,
    )
    return GETLOCATIONBEFORE
def getlist_before(update: Update, context: CallbackContext) -> int:    
    location = update.message.text
    context.chat_data['Location'] = location
    getlist = context.chat_data           
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    rc_in = 0
    for (k, v) in users.items():        
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):
            rc_in =+ 1
            update.message.reply_text(
                "Name: " + str(v["Name"]) + 
                "\nService Type: " + str(v["Type"]) +
                "\nLocation: " + str(v["Location"]) +
                "\nLink to chat: @{}".format(str(v["Username"])),
            )        
    if(rc_in==0):
        update.message.reply_text(
            "Sorry, none of our {} services are available at {} for the moment!".format(str(getlist["Type"]), str(getlist["Location"])),            
        )
        update.message.reply_text(                     
            "\nIs there anything else I can help you with?",            
            reply_markup=features,
        )
        return BEFORE_REG
   
    update.message.reply_text(
        "All the list of available {} services at {} have been sent. Is there anything else I can help you with?".format(str(getlist["Type"]), str(getlist["Location"])),        
        reply_markup=features,
    )
    return BEFORE_REG

#=========================================================MAKE A REQUEST=======================================================================#
def getservice_bef(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "What kind of services that you are searching for?",       
        reply_markup=getservice,
    )
    return GETSERVICEBEF
def getlocation_bef(update: Update, context: CallbackContext) -> int:
    service = update.message.text
    context.chat_data['Type'] = service
    update.message.reply_text(
        "Please select a location of your selected service:",       
        reply_markup=getlocation,
    )
    return GETLOCATIONBEF
def getmessage_bef(update: Update, context: CallbackContext) -> int:
    location = update.message.text
    context.chat_data['Location'] = location
    getlist = context.chat_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)    
    for (k, v) in users.items():
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):            
            update.message.reply_text(
                "Please write the request message that you want to send to all available {} services:".format(context.chat_data['Type']) +
                "\n\nEx,\nfrom Mahallah Zubair to LRT Gombak, at 2.30pm",
            )
            return GETMESSAGEBEF
    update.message.reply_text(
            "Sorry, none of our {} services are available at {} for the moment!".format(str(getlist["Type"]), str(getlist["Location"])),
        )
    update.message.reply_text(
        "\nIs there anything else I can help you with?",        
        reply_markup=features,
    )
    return BEFORE_REG
def sendrequest(update: Update, context: CallbackContext) -> int:
    url = "INSERT YOURS HERE"
    message = update.message.text
    context.chat_data["Message"] = message
    id = str(update.message.chat['id'])
    username = update.message.chat.username
    getlist = context.chat_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):
            if(str(k)!=str(id)):
                intro = [
                    "Hello {}, it seems like we have a client who is currently requesting for a service. Go get him/her now!".format(str(v["Name"])) +               
                    "\n\nClient's message:\n'{}'".format(message) +
                    "\n\nLink to chat: @{}".format(username),
                ]
                intro = {"chat_id": str(k), "text": intro}
                requests.post(url, data=intro)
    update.message.reply_text(
        "Your request has been successfully sent to all {} services that are currently available at {}.".format(str(getlist["Type"]), str(getlist["Location"])) +
        "\n\nPlease use the command 'Taken' to inform other {} services that your request has been taken.".format(str(getlist["Type"])),
        reply_markup=taken,
    )
    return TAKEN_BEFORE
def taken_before(update: Update, context: CallbackContext) -> int:
    url = "INSERT YOURS HERE"    
    username = update.message.chat.username
    id = str(update.message.chat['id'])
    getlist = context.chat_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)   
    for (k, v) in users.items():
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):           
            if(str(k)!=str(id)):
                intro = [
                    "This client's request has been taken!" +
                    "\n\nClient's message:\n'{}'".format(getlist["Message"]) +
                    "\n\nLink to chat: @{}".format(username),
                ]
                intro = {"chat_id": str(k), "text": intro}
                requests.post(url, data=intro)
    update.message.reply_text(
        "Your have successfully inform other {} services that your request has been taken.".format(str(getlist["Type"]))
    )
    update.message.reply_text(
        "\nIs there anything else I can help you with?",        
        reply_markup=features,
    )
    return BEFORE_REG
#========================================================FEEDBACK BEFORE=======================================================================#
def feedback_bef(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Please type in your review:",
        reply_markup=back,        
    )        
    return FEED_BEF
def send_feed_bef(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    context.bot_data['Message'] = update.message.text
    message = context.bot_data
    db.child("Feedback").child(id).set(message)
    update.message.reply_text(
        "Thank you for your feedback. We will always try to improve our product."
    )
    update.message.reply_text(
        "\nIs there anything else I can help you with?",        
        reply_markup=features,
    )
    return BEFORE_REG

#=========================================================BACK TO BEFORE=======================================================================#
def back_before(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Hi! I'm GetFalcon Bot. I'm here to provide a platform for you to get the list of your chosen services. What can I do for you?" +
        "\n\nIf you need any help on how to use this bot, please read our guidelines here @GetFalcon",        
        reply_markup=features,
    )
    return BEFORE_REG

#=========================================================after register=======================================================================#
#============================================================view info=========================================================================#
def viewinfo(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)    
    for (k, v) in users.items():
        if(str(k)==str(id)):
            update.message.reply_text(
                "Name: " + str(v["Name"]) +
                "\nService Type: " + str(v["Type"]) +
                "\nLocation: " + str(v["Location"]),
                reply_markup=after_reg,
            )
            return AFTER_REG

#===========================================================change info========================================================================#
def changeinfo(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Please select the information that you wish to change:",        
        reply_markup=update_info,
    )
    return GETINFO_CHANGE
def chg_name(update: Update, context: CallbackContext) -> int:
    context.user_data['Name']= ''
    update.message.reply_text(
        "Please enter your new Name:"
    )
    return CHANGENAME
def chg_service_type(update: Update, context: CallbackContext) -> int:
    context.user_data['Type']= ''    
    update.message.reply_text(
        'Please choose your new Service Type:',        
        reply_markup=service,
    )
    return CHANGETYPE
def chg_location(update: Update, context: CallbackContext) -> int:
    context.user_data['Location']= ''    
    update.message.reply_text(
        'Please choose your new Location:',        
        reply_markup=getlocation,
    )
    return CHANGELOCATION
def change_name(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    name = update.message.text
    context.user_data['Name'] = name
    user_data=context.user_data
    db.child("Employee").child(id).update(user_data)
    update.message.reply_text(
        "You have successfully change your Name to: {}".format(user_data['Name']),
    )
    update.message.reply_text(
        "Is there any other information that you wish to change?",        
        reply_markup=update_info,
    )
    return GETINFO_CHANGE
def change_type(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    type = update.message.text
    context.user_data['Type'] = type
    user_data=context.user_data
    db.child("Employee").child(id).update(user_data)
    update.message.reply_text(
        "You have successfully change your Service Type to: {}".format(user_data['Type']),        
    )
    update.message.reply_text(
        "Is there any other information that you wish to change?",        
        reply_markup=update_info,
    )
    return GETINFO_CHANGE
def change_location(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    location = update.message.text
    context.user_data['Location'] = location
    user_data=context.user_data
    db.child("Employee").child(id).update(user_data)
    update.message.reply_text(
        "You have successfully change your Location to: {}".format(user_data['Location']),        
    )
    update.message.reply_text(
        "Is there any other information that you wish to change?",        
        reply_markup=update_info,
    )
    return GETINFO_CHANGE

#============================================================get list==========================================================================#
def getservice_after(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "What kind of services that you are searching for?",              
        reply_markup=getservice,
    )
    return GETSERVICEAFTER
def getlocation_after(update: Update, context: CallbackContext) -> int:
    service = update.message.text
    context.chat_data['Type'] = service          
    update.message.reply_text(
        "Please select a location of your selected service:",          
        reply_markup=getlocation,
    )
    return GETLOCATIONAFTER
def getlist_after(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    location = update.message.text
    context.chat_data['Location'] = location
    getlist = context.chat_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    rc_in = 0
    for (k, v) in users.items():
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):
            rc_in =+ 1
            update.message.reply_text(
                "Name: " + str(v["Name"]) +
                "\nService Type: " + str(v["Type"]) +
                "\nLocation: " + str(v["Location"]) +
                "\nLink to chat: @{}".format(str(v["Username"])),
            )
    if(rc_in==0):
        update.message.reply_text(
            "Sorry, none of our {} services are available at {} for the moment!".format(str(getlist["Type"]), str(getlist["Location"])),
        )
        for (k, v) in users.items():
            if(str(k)==str(id)):
                update.message.reply_text(
                    "Is there anything else you would like to do, {}?".format(str(v["Name"])),
                    reply_markup=after_reg,
                )
                return AFTER_REG
    for (k, v) in users.items():
        if(str(k)==str(id)):
            update.message.reply_text(
                "All the list of available {} services at {} have been sent. Is there anything else you would like to do, {}?".format(str(getlist["Type"]), str(getlist["Location"]), str(v["Name"])),                
                reply_markup=after_reg,
            )
            return AFTER_REG

#=========================================================make a request=======================================================================#
def getservice_aft(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "What kind of services that you are searching for?",       
        reply_markup=getservice,
    )
    return GETSERVICEAFT
def getlocation_aft(update: Update, context: CallbackContext) -> int:
    service = update.message.text
    context.chat_data['Type'] = service
    update.message.reply_text(
        "Please select a location of your selected service:",
        reply_markup=getlocation,
    )
    return GETLOCATIONAFT
def getmessage_aft(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    location = update.message.text
    context.chat_data['Location'] = location
    getlist = context.chat_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)    
    for (k, v) in users.items():
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):            
            update.message.reply_text(
                "Please write the request message that you want to send to all available {} services:".format(context.chat_data['Type']) +
                "\n\nEx,\nfrom Mahallah Zubair to LRT Gombak, at 2.30pm",
            )
            return GETMESSAGEAFT
    update.message.reply_text(
            "Sorry, none of our {} services are available at {} for the moment!".format(str(getlist["Type"]), str(getlist["Location"])),
        )
    for (k, v) in users.items():        
        if(str(k)==str(id)):
            update.message.reply_text(
                "Is there anything else you would like to do, {}?".format(str(v["Name"])),                
                reply_markup=after_reg,
            )
            return AFTER_REG
def sendrequest_aft(update: Update, context: CallbackContext) -> int:
    url = "INSERT YOURS HERE"
    message = update.message.text
    context.chat_data["Message"] = message
    id = str(update.message.chat['id'])
    username = update.message.chat.username
    getlist = context.chat_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):
            if(str(k)!=str(id)):
                intro = [
                    "Hello {}, it seems like we have a client who is currently requesting for a service. Go get him/her now!".format(str(v["Name"])) +               
                    "\n\nClient's message:\n'{}'".format(message) +
                    "\n\nLink to chat: @{}".format(username),
                ]
                intro = {"chat_id": str(k), "text": intro}
                requests.post(url, data=intro)
    update.message.reply_text(
        "Your request has been successfully sent to all {} services that are currently available at {}.".format(str(getlist["Type"]), str(getlist["Location"])) +
        "\n\nPlease use the command 'Taken' to inform other {} services that your request has been taken.".format(str(getlist["Type"])),
        reply_markup=taken,
    )
    return TAKEN_AFTER
def taken_after(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    url = "INSERT YOURS HERE"    
    username = update.message.chat.username
    getlist = context.chat_data
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)   
    for (k, v) in users.items():
        if(str(v["Status"])=="Check-in" and str(v["Type"])==str(getlist["Type"]) and str(v["Location"])==str(getlist["Location"])):           
            if(str(k)!=str(id)):
                intro = [
                    "This client's request has been taken!".format(str(v["Name"])) +
                    "\n\nClient's message:\n'{}'".format(getlist["Message"]) +
                    "\n\nLink to chat: @{}".format(username),
                ]
                intro = {"chat_id": str(k), "text": intro}
                requests.post(url, data=intro)
    for (k, v) in users.items():
        if(str(k)==str(id)):
            update.message.reply_text(
                "Your have successfully inform other {} services that your request has been taken.".format(str(getlist["Type"]))
                )
            update.message.reply_text(
                "Is there anything else you would like to do, {}?".format(str(v["Name"])),                
                reply_markup=after_reg,
            )
            return AFTER_REG
    
#=========================================================update status========================================================================#
def update_status(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Use these two commands to update your availability:" +
        "\n\nCheck-in" +
        "\nCheck-out",      
        reply_markup=updatestatus,
    )
    return UPDATESTATUS
def check_in(update: Update, context: CallbackContext) -> int:
    id = update.message.chat.id
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)            
    for (k, v) in users.items():        
        if(str(k)==str(id) and str(v["Status"])=="Check-in"):
            update.message.reply_text(
                "Sorry, you have already Checked-in!",
                reply_markup=updatestatus
            )
            return UPDATESTATUS

        elif(str(k)==str(id) and str(v["Status"])!="Check-in"):
            db.child("Employee").child(id).update({"Status":"Check-in"})
            update.message.reply_text(
                "You have successfully Checked-in!",
                reply_markup=updatestatus
            )
            return UPDATESTATUS
def check_out(update: Update, context: CallbackContext) -> int:     
    id = update.message.chat.id
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)
    for (k, v) in users.items():
        if(str(k)==str(id) and str(v["Status"])=="Check-out"):
            update.message.reply_text(
                "Sorry, you have already Checked-out!",
                reply_markup=updatestatus
            )
            return UPDATESTATUS
        
        elif(str(k)==str(id) and str(v["Status"])!="Check-out"):
            db.child("Employee").child(id).update({"Status":"Check-out"})
            update.message.reply_text(
                "You have successfully Checked-out!",
                reply_markup=updatestatus
            )
            return UPDATESTATUS

#=========================================================feedback after========================================================================#
def feedback_aft(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Please type in your review:",
        reply_markup=back,
    )
    return FEED_AFT
def send_feed_aft(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    context.bot_data['Message'] = update.message.text
    message = context.bot_data
    db.child("Feedback").child(id).set(message)
    update.message.reply_text(
        "Thank you for your feedback. We will always try to improve our product."
    )
    update.message.reply_text(
        "\nIs there anything else I can help you with?",        
        reply_markup=after_reg,
    )
    return AFTER_REG

#=========================================================back to after========================================================================#
def back_after(update: Update, context: CallbackContext) -> int:
    id = str(update.message.chat['id'])
    users = db.child("Employee").get()
    users = users.val()
    users = json.dumps(users, indent=2)
    users = json.loads(users)    
    for (k, v) in users.items():        
        if(str(k)==str(id)):
            update.message.reply_text(
                "Hello {}, what can I do for you?".format(str(v["Name"])) +
                "\n\nIf you need any help on how to use this bot, please read our guidelines here @GetFalcon",                
                reply_markup=after_reg,
            )
            return AFTER_REG

#=============================================================EXIT=============================================================================#
def exits(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "You have exited. All commands have been disabled.\n\nPlease use the /start command to start a new conversation with our bot.",
    )
    return ConversationHandler.END

#=============================================================MAIN=============================================================================#
def main() -> None:
    token = "INSERT YOURS HERE"
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={

#========================================================BEFORE REGISTER=======================================================================#         

            BEFORE_REG: [
                MessageHandler(Filters.regex('^Register <for service providers>$'), verification),            
                MessageHandler(Filters.regex('^Get List$'), getservice_before),
                MessageHandler(Filters.regex('^Send a Request$'), getservice_bef),
                MessageHandler(Filters.regex('^Give Feedback$'), feedback_bef),                
            ],
#==========================================================REGISTRATION========================================================================#            
            
            CHECKCODE_REG: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Back$')), checkcode),
                MessageHandler(Filters.regex('^Back$'),back_before)
            ],
            GETINFO_REG: [
                MessageHandler(Filters.regex('^Name$'), name),
                MessageHandler(Filters.regex('^Service Type$'), service_type),
                MessageHandler(Filters.regex('^Location$'), location),
                MessageHandler(Filters.regex('^Cancel$'), back_before),
            ],
            NAME_REG: [MessageHandler(Filters.text, enter_name)],
            TYPE_REG: [
                MessageHandler(Filters.regex('^Runner$'), enter_type),
                MessageHandler(Filters.regex('^Transporter$'), enter_type),
            ],
            LOCATION_REG: [                
                MessageHandler(Filters.regex('^IIUM Gombak$'), enter_location),
                MessageHandler(Filters.regex('^IIUM Kuantan$'), enter_location),
                MessageHandler(Filters.regex('^IIUM Gambang$'), enter_location),
                MessageHandler(Filters.regex('^IIUM Pagoh$'), enter_location),
            ],
            CONFIRM_REG: [
                MessageHandler(Filters.regex('^Name$'), name),
                MessageHandler(Filters.regex('^Service Type$'), service_type),
                MessageHandler(Filters.regex('^Location$'), location),
                MessageHandler(Filters.regex('^Cancel$'), back_before),
                MessageHandler(Filters.regex('^Confirm$'), confirms),                
            ],
#=============================================================GET LIST=========================================================================#
            
            GETLOCATIONBEFORE: [
                MessageHandler(Filters.regex('^IIUM Gombak$'), getlist_before),
                MessageHandler(Filters.regex('^IIUM Kuantan$'), getlist_before),
                MessageHandler(Filters.regex('^IIUM Gambang$'), getlist_before),
                MessageHandler(Filters.regex('^IIUM Pagoh$'), getlist_before),
            ],
            GETSERVICEBEFORE : [
                MessageHandler(Filters.regex('^Back$'),back_before),
                MessageHandler(Filters.regex('^Runner$'), getlocation_before),
                MessageHandler(Filters.regex('^Transporter$'), getlocation_before),
            ],
#=========================================================REQUEST MENU=========================================================================#            
            
            GETLOCATIONBEF: [
                MessageHandler(Filters.regex('^IIUM Gombak$'), getmessage_bef),
                MessageHandler(Filters.regex('^IIUM Kuantan$'), getmessage_bef),
                MessageHandler(Filters.regex('^IIUM Gambang$'), getmessage_bef),
                MessageHandler(Filters.regex('^IIUM Pagoh$'), getmessage_bef),
            ],
            GETSERVICEBEF: [
                MessageHandler(Filters.regex('^Back$'),back_before),
                MessageHandler(Filters.regex('^Runner$'), getlocation_bef),
                MessageHandler(Filters.regex('^Transporter$'), getlocation_bef),
            ],
            GETMESSAGEBEF: [MessageHandler(Filters.text, sendrequest)],
            TAKEN_BEFORE: [MessageHandler(Filters.regex('^Taken$'), taken_before)],
            FEED_BEF: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Back$') | Filters.regex('^Exit$')), send_feed_bef),
                MessageHandler(Filters.regex('^Back$'),back_before),
            ],           

#=========================================================AFTER REGISTER=======================================================================#

            AFTER_REG: [
                MessageHandler(Filters.regex('^View Information$'), viewinfo), 
                MessageHandler(Filters.regex('^Change Information$'), changeinfo), 
                MessageHandler(Filters.regex('^Get List$'), getservice_after),
                MessageHandler(Filters.regex('^Send a Request$'), getservice_aft),
                MessageHandler(Filters.regex('^Update Status$'), update_status),
                MessageHandler(Filters.regex('^Give Feedback$'), feedback_aft),                          
            ],
#===========================================================CHANGE INFO========================================================================#
            
            GETINFO_CHANGE: [
                MessageHandler(Filters.regex('^Name$'), chg_name),
                MessageHandler(Filters.regex('^Service Type$'), chg_service_type),
                MessageHandler(Filters.regex('^Location$'), chg_location),
                MessageHandler(Filters.regex('^Back$'), back_after),
            ],
            CHANGENAME: [MessageHandler(Filters.text, change_name)],
            CHANGETYPE: [                
                MessageHandler(Filters.regex('^Runner$'), change_type),
                MessageHandler(Filters.regex('^Transporter$'), change_type),
            ],
            CHANGELOCATION: [                
                MessageHandler(Filters.regex('^IIUM Gombak$'), change_location),
                MessageHandler(Filters.regex('^IIUM Kuantan$'), change_location),
                MessageHandler(Filters.regex('^IIUM Gambang$'), change_location),
                MessageHandler(Filters.regex('^IIUM Pagoh$'), change_location),
            ],
#=============================================================GET LIST=========================================================================

            GETLOCATIONAFTER: [
                MessageHandler(Filters.regex('^IIUM Gombak$'), getlist_after),
                MessageHandler(Filters.regex('^IIUM Kuantan$'), getlist_after),
                MessageHandler(Filters.regex('^IIUM Gambang$'), getlist_after),
                MessageHandler(Filters.regex('^IIUM Pagoh$'), getlist_after),
            ],
            GETSERVICEAFTER : [
                MessageHandler(Filters.regex('^Runner$'), getlocation_after),
                MessageHandler(Filters.regex('^Transporter$'), getlocation_after),
                MessageHandler(Filters.regex('^Back$'), back_after),
            ],
#=========================================================REQUEST MENU=========================================================================#            
            
            GETLOCATIONAFT: [
                MessageHandler(Filters.regex('^IIUM Gombak$'), getmessage_aft),
                MessageHandler(Filters.regex('^IIUM Kuantan$'), getmessage_aft),
                MessageHandler(Filters.regex('^IIUM Gambang$'), getmessage_aft),
                MessageHandler(Filters.regex('^IIUM Pagoh$'), getmessage_aft),
            ],
            GETSERVICEAFT: [
                MessageHandler(Filters.regex('^Runner$'), getlocation_aft),
                MessageHandler(Filters.regex('^Transporter$'), getlocation_aft),
                MessageHandler(Filters.regex('^Back$'), back_after),
            ],
            GETMESSAGEAFT: [MessageHandler(Filters.text, sendrequest_aft)],
            TAKEN_AFTER: [MessageHandler(Filters.regex('^Taken$'), taken_after)],
            
            FEED_AFT: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Back$') | Filters.regex('^Exit$')), send_feed_aft),
                MessageHandler(Filters.regex('^Back$'),back_after),
            ], 
#==========================================================UPDATE STATUS=======================================================================#

            UPDATESTATUS: [                    
                MessageHandler(Filters.regex('^Check-in$'), check_in),
                MessageHandler(Filters.regex('^Check-out$'), check_out),
                MessageHandler(Filters.regex('^Back$'), back_after),
            ],
        },

        fallbacks=[           
            MessageHandler(Filters.regex('^Exit$'), exits),
            ],
    )
    dispatcher.add_handler(conv_handler)
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=token)
    updater.bot.setWebhook('INSERT YOURS HERE' + token)
    updater.idle()

if __name__ == '__main__':
    while True:
        main()
