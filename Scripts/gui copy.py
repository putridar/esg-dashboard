import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
import requests

import refinitiv
import unpri
#import summary

## FIREBASE
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.realpath("group18---natwest-firebase.json")

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("group18---natwest-firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#get document id for green bond
doc_ref = list(db.collection("asian bank").get())
#document id
ids = []
for x in doc_ref:
  ids.append(x.id)

## DATA FROM FIREBASE
green_bond = {}
unpri_data = {}
summary = {}

for x in ids:
  doc = db.collection("asian bank").document(x).get()
  if doc.exists:
    curr = doc.to_dict()
    if "green bond" in curr:
      green_bond[x] = curr['green bond']
    if "unpri" in curr:
      unpri_data[x] = curr['unpri']
    if "summary" in curr:
      summary[x] = curr['summary']
      
window = Tk()

window.geometry("1371x814")
window.configure(bg = "#FFFFFF")

## FUNCTION
def click():
    esg_rating = refinitiv.RefinitivList(variable.get())

    esg_score = esg_rating[2][-2:]
    env_score = esg_rating[5][-2:]
    social_score = esg_rating[10][-2:]
    gov_score = esg_rating[16][-2:]

    ## ESG RATING

    #boxes
    canvas.create_rectangle(350.0,357.0, 516.0, 465.0, fill="#F5F4FD",outline="")
    canvas.create_rectangle(910.0,357.0,1076.0,465.0,fill="#F5F4FD",outline="")
    canvas.create_rectangle( 540.0,357.0,706.0,465.0,fill="#F5F4FD",outline="")
    canvas.create_rectangle(725.0,357.0,891.0,465.0,fill="#F5F4FD",outline="")
    #label
    canvas.create_text(400.0,370.0,anchor="nw",text="Overall",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    canvas.create_text(941.0,369.0,anchor="nw",text="Governance",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    canvas.create_text(568.0,369.0,anchor="nw",text="Environment",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    canvas.create_text(782.0,369.0,anchor="nw",text="Social",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    #values
    canvas.create_text(405.0, 393.0, anchor="nw",text=esg_score, fill="#90D27F",
                       font=("Raleway SemiBold", 48 * -1))
    canvas.create_text(595.0,393.0,anchor="nw",text=env_score,fill="#FF8080",
                       font=("Raleway SemiBold", 48 * -1))
    canvas.create_text(780.0,393.0,anchor="nw",text=social_score,fill="#FFAD71",
                       font=("Raleway SemiBold", 48 * -1))
    canvas.create_text(965.0, 393.0,anchor="nw", text=gov_score, fill="#90D27F",
                       font=("Raleway SemiBold", 48 * -1))

    ## DATA FROM UNPRI

    print(unpri_data)
    canvas.create_text(822.0,617.0,anchor="nw",text="1",fill="#000000",
                       font=("Raleway Regular", 14 * -1))
    canvas.create_text(867.0,619.0,anchor="nw",text="UNPRI",fill="#000000", font=("Raleway Regular", 12 * -1))

    if (unpri_data[variable.get()] == 'Yes'):
        print("masuk sini")
        joined = PhotoImage(file=relative_to_assets("image_8.png"))
        joined_create = canvas.create_image(1160.0,625.0,image=joined)
        logo_label = tk.Label(image=joined_create, bg = "#401564")
    else:
        print("masuk sana")
        logo = Image.open(file=relative_to_assets("image_9.png"))
        #logo = logo.resize((int(logo.size[0]/4),int(logo.size[1]/4)))
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg = "#401564")
        logo_label.image = logo
        logo_label.place(1160.0, 660.0)

        #image_image_9 = PhotoImage(file=relative_to_assets("image_9.png"))
        #image_9 = canvas.create_image(1160.0,660.0,image=image_image_9)

    

    ## COMPANY LOGO

    #logo = Image.open('ocbc-pic.png')
    #logo = logo.resize((int(logo.size[0]/3),int(logo.size[1]/3)))
    #logo = ImageTk.PhotoImage(logo)
    #logo_label = tk.Label(image=logo, bg = "white")
    #logo_label.image = logo
    #logo_label.place(x=800, y=100)

    ## TEXT SUMMARY

    canvas.create_text(359.0, 214.0, anchor="nw",text="Summary",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    #canvas.create_text(359.0, 243.0,anchor="nw",text=summary.get_summary(variable.get()),fill="#BCBCBC",
                       #font=("Raleway Bold", 14 * -1))

#HEADER
    
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 814,
    width = 1371,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)


canvas.create_text(
    359.0,
    91.0,
    anchor="nw",
    text="Performance based on ratings,  ESG Keywords, and Ratings",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    805.0,
    572.0,
    1227.0,
    770.0,
    fill="#F5F4FD",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    295.0,
    900.0,
    fill="#F4F4FC",
    outline="")

canvas.create_text(
    359.0,
    45.0,
    anchor="nw",
    text="Companies’ ESG Performance",
    fill="#192159",
    font=("Raleway Bold", 36 * -1)
)

canvas.create_text(
    24.0,
    160.0,
    anchor="nw",
    text="List of Companies",
    fill="#192159",
    font=("Raleway Bold", 14 * -1)
)

canvas.create_text(
    361.0,
    135.0,
    anchor="nw",
    text="Company: DBS",
    fill="#7B85F7",
    font=("Raleway SemiBold", 24 * -1)
)

canvas.create_text(
    102.0,
    42.0,
    anchor="nw",
    text="NatWest Markets",
    fill="#192159",
    font=("Raleway Bold", 18 * -1)
)

canvas.create_text(
    359.0,
    528.0,
    anchor="nw",
    text="ESG Keywords",
    fill="#192159",
    font=("Raleway Bold", 18 * -1)
)

canvas.create_text(
    805.0,
    528.0,
    anchor="nw",
    text="Membership Table",
    fill="#192159",
    font=("Raleway Bold", 18 * -1)
)



canvas.create_text(
    359.0,
    174.0,
    anchor="nw",
    text="Continent: Asia",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)

canvas.create_text(
    483.0,
    174.0,
    anchor="nw",
    text="Country: Japan",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)



canvas.create_text(
    822.0,
    652.0,
    anchor="nw",
    text="2",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)

canvas.create_text(
    867.0,
    654.0,
    anchor="nw",
    text="ShengShiong membership",
    fill="#000000",
    font=("Raleway Regular", 12 * -1)
)

variable = tk.StringVar(window)
variable.set("ocbc") # default value

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    152.865478515625,
    125.09860229492188,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    textvariable=variable,
    highlightthickness=0
)
entry_1.place(
    x=24.0,
    y=106.0,
    width=257.73095703125,
    height=36.19720458984375
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=click,
    relief="flat"
)
button_1.place(
    x=245.0,
    y=112.0,
    width=28.0,
    height=28.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    51.0,
    52.0,
    image=image_image_1
)

canvas.create_rectangle(
    0.0,
    185.0,
    295.0,
    242.0,
    fill="#D9D7EF",
    outline="")

canvas.create_text(
    76.0,
    205.0,
    anchor="nw",
    text="DBS",
    fill="#401564",
    font=("Raleway Bold", 14 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    44.0,
    213.0,
    image=image_image_2
)

canvas.create_text(
    76.0,
    261.0,
    anchor="nw",
    text="OCBC",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    44.0,
    269.0,
    image=image_image_3
)

canvas.create_text(
    76.0,
    317.0,
    anchor="nw",
    text="UOB",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    44.0,
    325.0,
    image=image_image_4
)

canvas.create_text(
    361.0,
    324.0,
    anchor="nw",
    text="ESG Rating",
    fill="#192159",
    font=("Raleway Bold", 18 * -1)
)







image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    438.0,
    490.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    631.0,
    490.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    818.0,
    490.0,
    image=image_image_7
)

canvas.create_rectangle(
    805.0,
    572.0,
    1227.0,
    602.0,
    fill="#F4F4FC",
    outline="")

canvas.create_rectangle(
    846.0,
    572.0,
    846.0,
    786.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1096.0,
    572.0,
    1096.0,
    786.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    816.0,
    580.0,
    anchor="nw",
    text="No.",
    fill="#AE99C0",
    font=("Raleway SemiBold", 12 * -1)
)

canvas.create_text(
    867.0,
    580.0,
    anchor="nw",
    text="Membership Name",
    fill="#AE99C0",
    font=("Raleway SemiBold", 12 * -1)
)

canvas.create_text(
    1111.0,
    580.0,
    anchor="nw",
    text="Status",
    fill="#AE99C0",
    font=("Raleway SemiBold", 12 * -1)
)





image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    515.0,
    675.0,
    image=image_image_10
)

canvas.create_rectangle(
    547.0,
    133.0,
    577.0,
    163.0,
    fill="#AE99C0",
    outline="")
window.resizable(False, False)
window.mainloop()
