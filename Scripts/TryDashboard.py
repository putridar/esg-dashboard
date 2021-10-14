import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
import requests

import refinitiv
import unpri

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.realpath("group18---natwest-firebase.json")

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("group18---natwest-firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

#get document id for green bond
doc_ref = list(db.collection("green bond").get())
#document id
ids = []
for x in doc_ref:
  ids.append(x.id)


#keydown function
def click():
    esg_rating = refinitiv.RefinitivList(variable.get())

    esg_score = esg_rating[2]
    env_score = esg_rating[5]
    social_score = esg_rating[10]
    gov_score = esg_rating[16]

    esg_values = [esg_score, env_score, social_score, gov_score]

    place_x = 10
    place_y = 160

    ## ESG RATING
    
    for i in range(0, len(esg_values)):
        rating_box = tk.Canvas(window, width=150, height=100, bg='#401564', highlightthickness=0).place(x=place_x, y=place_y)
        tk.Label(rating_box, text=esg_values[i][:-2], font='Montserrat 12', bg='#401564',
             fg='#FFFFFF').place(x=place_x, y=place_y)
        tk.Label(rating_box, text=esg_values[i][-2:], font='Montserrat 40', bg='#401564',
             fg='#FFFFFF').place(x=place_x, y=place_y+20)
        place_x += 170

    ## DATA FROM FIREBASE
    data = {}
    for x in ids:
      doc = db.collection("green bond").document(x).get()
      if doc.exists:
        curr = doc.to_dict()
        data[x] = curr['value']

    green_bond_box = tk.Canvas(window, width=150, height=100, bg='#401564', highlightthickness=0).place(x=10, y=300)
    tk.Label(green_bond_box, text='Green Bond', font='Montserrat 12', bg='#401564',
        fg='#FFFFFF').place(x=10, y=300)
    tk.Label(green_bond_box, text=data[variable.get()], font='Montserrat 23', bg='#401564',
        fg='#FFFFFF').place(x=10, y=330)

    ## DATA FROM UNPRI

    unpri_box = tk.Canvas(window, width=150, height=100, bg='#401564', highlightthickness=0).place(x=180, y=300)
    tk.Label(unpri_box, text='UNPRI Member', font='Montserrat 12', bg='#401564',
        fg='#FFFFFF').place(x=180, y=300)
    tk.Label(unpri_box, text=unpri.is_member(variable.get()), font='Montserrat 23', bg='#401564',
        fg='#FFFFFF').place(x=180, y=330)

    ## COMPANY LOGO

    logo = Image.open('ocbc-pic.png')
    logo = logo.resize((int(logo.size[0]/3),int(logo.size[1]/3)))
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo, bg = "white")
    logo_label.image = logo
    logo_label.place(x=800, y=100)

## Initiate Window
window = tk.Tk()
window.title("ESG Dashboard")
window.geometry('1305x780')

## Header
top_bg = tk.Canvas(window, width=1305, height=70, bg="#401564", highlightthickness=0).place(x=0, y=0)


## Company Logo
logo = Image.open('natwest-logo.png')
logo = logo.resize((int(logo.size[0]/4),int(logo.size[1]/4)))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo, bg = "#401564")
logo_label.image = logo
logo_label.grid(column=0, row=0, pady=2)

## Title of Dashboard
tk.Label(window, text='Companies\' ESG Performance', font='Montserrat 25', bg='#401564', fg='white').\
               grid(column=6, row=0, pady=2)


tk.Label(window, text="Enter the company name you want to search for: ").place(x=0, y=70)

## Dropdown
variable = tk.StringVar(window)
variable.set("ocbc") # default value

w = tk.OptionMenu(window, variable, "ocbc", "dbs", "uob")
w.place(x=0, y=90)

## Submit Button
tk.Button(window, text="Submit", width = 6, command = click).place(x=80, y=90)

    
window.mainloop()


