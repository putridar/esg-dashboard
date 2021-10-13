import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
import requests

#import weather2
#import piholeget
#import hddspace
#import steam
#import news
#import xplane
import refinitiv

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.realpath("group18---natwest-firebase-adminsdk-r6242-f0f0ebcfbf.json")

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("group18---natwest-firebase-adminsdk-r6242-f0f0ebcfbf.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#get document id for green bond
doc_ref = list(db.collection("green bond").get())
#document id
ids = []
for x in doc_ref:
  ids.append(x.id)


#keydown function
def click_rating():
    #entered_text = textentry.get()
    esg_rating = refinitiv.RefinitivList(variable.get())

    value = 160
    rating_x = 10
    rating_box = tk.Canvas(window, width=590, height=480, bg='#A63A50', highlightthickness=0).place(x=rating_x, y=value)
    rating_box_top = tk.Canvas(window, width=590, height=20, bg='#1b2838', highlightthickness=0).place(x=rating_x, y=value-20)
    #rating_box_price = tk.Canvas(rating_box, width=80, height=520, bg='#171a21', highlightthickness=0).place(x=rating_x, y=value)
    tk.Label(rating_box_top, text='ESG Rating', font='Montserrat 7 bold', bg='#1b2838',
             fg='#FFFFFF').place(x=10, y=value-20)
    
    steam_y = 160
    for i in range(0, len(esg_rating)):
        my_text = tk.Label(rating_box, text=esg_rating[i], font='Montserrat 12', bg='#A63A50',
             fg='#FFFFFF').place(x=rating_x, y=steam_y)
        steam_y += 20

## MAKE WINDOW
window = tk.Tk()
window.title("ESG Dashboard")
window.geometry('1305x780')

# DRAW TOP BLUE BAR - DRAW TITLE - DRAW DATETIME
top_bg = tk.Canvas(window, width=1305, height=60, bg='#A63A50', highlightthickness=0).place(x=0, y=0)
tk.Label(top_bg, text='Companies\' ESG Performance', font='Montserrat 25', bg='#A63A50', fg='white').place(x=15, y=3)
tk.Label(top_bg, text=datetime.now().strftime('%A, %d %B %Y'), font='Montserrat 20', bg='#A63A50', fg='white').place(
    x=950, y=8)

## COMPANY'S LOGO
##photo = ImageTk.PhotoImage(Image.open("ocbc-pic.png").\
##                           resize((100, 50), Image.ANTIALIAS))
##Label (window, image = photo).grid(row = 0, column = 0)

##

##company_name = input("Enter the company name you want to search for: " )

tk.Label(window, text="Enter the company name you want to search for: ").place(x=0, y=60)

#text entry

#textentry = tk.Entry(window, width = 20, bg = "white")
#textentry.grid(row = 70, column = 0)
#textentry.place(x=0, y=80)

esg_rating=[]



value = 160
rating_x = 10
rating_box = tk.Canvas(window, width=590, height=480, bg='#A63A50', highlightthickness=0).place(x=rating_x, y=value)
rating_box_top = tk.Canvas(window, width=590, height=20, bg='#1b2838', highlightthickness=0).place(x=rating_x, y=value-20)
#rating_box_price = tk.Canvas(rating_box, width=80, height=520, bg='#171a21', highlightthickness=0).place(x=rating_x, y=value)
tk.Label(rating_box_top, text='ESG Rating', font='Montserrat 7 bold', bg='#1b2838',
         fg='#FFFFFF').place(x=10, y=value-20)


## DROP DOWN THINGS

variable = tk.StringVar(window)
variable.set("ocbc") # default value

w = tk.OptionMenu(window, variable, "ocbc", "dbs", "apple")
w.place(x=0, y=80)
#w.pack()

#add submit button 
tk.Button(window, text="Submit", width = 6, command = click_rating).place(x=0, y=110)
## print(esg_rating)
## REFINITIV

#read data from firebase
data = {}
for x in ids:
  doc = db.collection("green bond").document(x).get()
  if doc.exists:
    curr = doc.to_dict()
    data[x] = curr['value']

tk.Label(window, text=data[variable.get()]).place(x=100,y=110)
    
window.mainloop()


