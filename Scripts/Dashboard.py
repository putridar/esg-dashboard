import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
import requests

import refinitiv
import unpri
import unep_fi
import summary
import icma
import ungc
import iigcc

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
#green_bond = {}
#unpri_data = {}
## summary = {}

#for x in ids:
  #doc = db.collection("asian bank").document(x).get()
  #if doc.exists:
  #curr = doc.to_dict()
    #if "green bond" in curr:
    #  green_bond[x] = curr['green bond']
    #if "unpri" in curr:
     # unpri_data[x] = curr['unpri']
    #if "summary" in curr:
      #summary[x] = curr['summary']
      
window = Tk()

window.title("ESG Dashboard")
window.geometry("1371x814")
window.configure(bg = "#FFFFFF")

## FUNCTION
def click():

    canvas.create_rectangle(359.0,210.0, 1500.0, 350.0, fill="#FFFFFF",outline="")

    #COMPANY PROFILE
    #canvas.create_text(361.0,135.0,anchor="nw",text="Company: "+variable.get().upper(),
                       #fill="#7B85F7",font=("Raleway SemiBold", 24 * -1))
    canvas.create_rectangle(361.0,135.0, 900.0, 200.0, fill="#FFFFFF",outline="")
    comp_name = canvas.create_text(361.0,135.0,anchor="nw",
                                   text="Company: "+variable.get().upper(),
                                   fill="#7B85F7",font=("Raleway SemiBold", 24 * -1))
    #box_comp=canvas.create_rectangle(canvas.bbox(comp_name),fill="white",
    #                                 outline="white")
    #canvas.tag_lower(box_comp,comp_name)

    canvas.create_text(359.0,174.0,anchor="nw",text="Continent: Asia",
                       fill="#000000",font=("Raleway Regular", 14 * -1))
    canvas.create_text(483.0,174.0,anchor="nw",text="Country: Singapore",
                       fill="#000000",font=("Raleway Regular", 14 * -1))

     ## TEXT SUMMARY
    canvas.create_rectangle(359.0,210.0, 1500.0, 350.0, fill="#FFFFFF",outline="")
    canvas.create_text(359.0, 210.0, anchor="nw",text="ESG Facts",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    sum_label = tk.Label(window, text=summary.get_summary(variable.get()), font=("Raleway Bold", 14 * -1),
                 wraplength=900, justify="left", fg="#BCBCBC")
    sum_label.place(x=355, y=230)
    #canvas.create_text(359.0, 243.0,anchor="nw",
    #                   text= summary_text,
     #                  fill="#BCBCBC",
     #                  font=("Raleway Bold", 14 * -1))

    #ESG RATING

    esg_rating = refinitiv.RefinitivList(variable.get())
    
    if (esg_rating == 'NA'):
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
        
        canvas.create_text(405.0, 393.0, anchor="nw",text='NA', fill="#192159",
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(595.0,393.0,anchor="nw",text='NA',fill="#192159",
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(780.0,393.0,anchor="nw",text='NA',fill="#192159",
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(965.0, 393.0,anchor="nw", text='NA', fill="#192159",
                           font=("Raleway SemiBold", 48 * -1))
    else:
        esg_score = esg_rating[1][-2:]
        env_score = esg_rating[2][-2:]
        social_score = esg_rating[3][-2:]
        gov_score = esg_rating[4][-2:]

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
        def what_color(score):
            if (score < 30):
                return "#FF8080"
            elif (score < 60):
                return "#FFAD71"
            else:
                return "#90D27F"
        
        canvas.create_text(405.0, 393.0, anchor="nw",text=esg_score, fill=what_color(int(esg_score)),
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(595.0,393.0,anchor="nw",text=env_score,fill=what_color(int(env_score)),
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(780.0,393.0,anchor="nw",text=social_score,fill=what_color(int(social_score)),
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(965.0, 393.0,anchor="nw", text=gov_score, fill=what_color(int(gov_score)),
                           font=("Raleway SemiBold", 48 * -1))
    #info color
    image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(438.0,490.0,image=image_image_5)

    image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(631.0,490.0,image=image_image_6)

    image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(818.0,490.0,image=image_image_7)

    ## UNPRI

    canvas.create_text(822.0,617.0,anchor="nw",text="1",fill="#000000",
                       font=("Raleway Regular", 14 * -1))
    canvas.create_text(867.0,619.0,anchor="nw",text="UNPRI",fill="#000000", font=("Raleway Regular", 12 * -1))

    if (unpri.is_member(variable.get()) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=610)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=610)

    ## UNEP FI
    canvas.create_text(822.0,645.0,anchor="nw",text="2",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,648.0,anchor="nw",text="UNEP FI",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (unep_fi.is_member_unepfi(variable.get()) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=640)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=640)

    ## ICMA
    canvas.create_text(822.0,678.0,anchor="nw",text="3",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,680.0,anchor="nw",text="ICMA",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (icma.is_member_icma(variable.get()) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=670)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=670)

    ## IIGCC
    canvas.create_text(822.0,707.0,anchor="nw",text="4",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,709.0,anchor="nw",text="IIGCC",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (iigcc.is_member_iigcc(variable.get()) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=700)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=700)

    ## UNGC
    canvas.create_text(822.0,738.0,anchor="nw",text="5",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,740.0,anchor="nw",text="UNGC",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (ungc.is_member_ungc(variable.get()) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=730)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=730)
    ## COMPANY LOGO

    #logo = Image.open('ocbc-pic.png')
    #logo = logo.resize((int(logo.size[0]/3),int(logo.size[1]/3)))
    #logo = ImageTk.PhotoImage(logo)
    #logo_label = tk.Label(image=logo, bg = "white")
    #logo_label.image = logo
    #logo_label.place(x=800, y=100)

   

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

##canvas.create_text(
##    24.0,
##    160.0,
##    anchor="nw",
##    text="List of Companies",
##    fill="#192159",
##    font=("Raleway Bold", 14 * -1)
##)

canvas.create_text(
    361.0,
    135.0,
    anchor="nw",
    text="Company: ",
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
    text="Continent: ",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)

canvas.create_text(
    483.0,
    174.0,
    anchor="nw",
    text="Country: ",
    fill="#000000",
    font=("Raleway Regular", 14 * -1)
)





variable = tk.StringVar(window)
#variable.set("ocbc") # default value

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

##canvas.create_rectangle(
##    0.0,
##    185.0,
##    295.0,
##    242.0,
##    fill="#D9D7EF",
##    outline="")
##
##canvas.create_text(
##    76.0,
##    205.0,
##    anchor="nw",
##    text="DBS",
##    fill="#401564",
##    font=("Raleway Bold", 14 * -1)
##)
##
##image_image_2 = PhotoImage(
##    file=relative_to_assets("image_2.png"))
##image_2 = canvas.create_image(
##    44.0,
##    213.0,
##    image=image_image_2
##)
##
##canvas.create_text(
##    76.0,
##    261.0,
##    anchor="nw",
##    text="OCBC",
##    fill="#000000",
##    font=("Raleway Regular", 14 * -1)
##)
##
##image_image_3 = PhotoImage(
##    file=relative_to_assets("image_3.png"))
##image_3 = canvas.create_image(
##    44.0,
##    269.0,
##    image=image_image_3
##)
##
##canvas.create_text(
##    76.0,
##    317.0,
##    anchor="nw",
##    text="UOB",
##    fill="#000000",
##    font=("Raleway Regular", 14 * -1)
##)
##
##image_image_4 = PhotoImage(
##    file=relative_to_assets("image_4.png"))
##image_4 = canvas.create_image(
##    44.0,
##    325.0,
##    image=image_image_4
##)

canvas.create_text(
    361.0,
    324.0,
    anchor="nw",
    text="ESG Rating",
    fill="#192159",
    font=("Raleway Bold", 18 * -1)
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


#info color
image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(438.0,490.0,image=image_image_5)

image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(631.0,490.0,image=image_image_6)

image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(818.0,490.0,image=image_image_7)


image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    515.0,
    675.0,
    image=image_image_10
)

#canvas.create_rectangle(
    #547.0,
    #133.0,
    #577.0,
    #163.0,
    #fill="#AE99C0",
    #outline="")
window.resizable(False, False)
window.mainloop()
