import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO
from tkhtmlview import HTMLLabel
from urllib.request import Request, urlopen
import requests
from flask import request
from six.moves import urllib
import urllib
from time import sleep

import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import refinitiv
import unpri
import unep_fi
import summary
import icma
import ungc
import iigcc
import topic_model
import logo

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
      
window = Tk()

window.title("ESG Dashboard")
window.geometry("1371x814")
window.configure(bg = "#FFFFFF")

##################
## FUNCTIONS
##################


def unavailable_refinitiv():
    canvas.create_rectangle(350.0,270.0, 1200.0, 380.0, fill="black",outline="")
    canvas.create_text(600.0, 310.0,anchor="nw",text='Sorry, the ESG Rating is unavailable',fill="white",
                           font=("Raleway SemiBold", 18 * -1))
    
def show_esg_rating(input_company) :
    esg_rating = refinitiv.RefinitivList(input_company)
    
    #title
    canvas.create_text(361.0,324.0,anchor="nw",text="ESG Rating",
                       fill="#192159",font=("Raleway Bold", 18 * -1))
    #bigbox
    canvas.create_rectangle(350.0,270.0, 1200.0, 380.0, fill="white",outline="")
    #boxes
    canvas.create_rectangle(350.0,270.0, 516.0, 380.0, fill="#401564",outline="")
    canvas.create_rectangle(910.0,270.0,1076.0,380.0,fill="#F5F4FD",outline="")
    canvas.create_rectangle(540.0,270.0,706.0,380.0,fill="#F5F4FD",outline="")
    canvas.create_rectangle(725.0,270.0,891.0,380.0,fill="#F5F4FD",outline="")
    #label
    canvas.create_text(400.0,280.0,anchor="nw",text="Overall",fill="#FFFFFF",
                       font=("Raleway Bold", 18 * -1))
    canvas.create_text(572.0,280.0,anchor="nw",text="Environment",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    canvas.create_text(782.0,280.0,anchor="nw",text="Social",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    canvas.create_text(947.0,280.0,anchor="nw",text="Governance",fill="#192159",
                       font=("Raleway Bold", 18 * -1))
    
    if (esg_rating == 'NA'):
        unavailable_refinitiv()
    else:
        esg_score = esg_rating[1][-2:]
        env_score = esg_rating[2][-2:]
        social_score = esg_rating[3][-2:]
        gov_score = esg_rating[4][-2:]
        esg_rank = esg_rating[5].split(':')[1]
        actual_rank = int(esg_rank.split('/')[0][1:])
        industry = int(esg_rank.split('/')[1])

        #values
        def what_color():
            per30 = int(industry * 3 / 10)
            per70 = int(industry * 7 / 10)
            if (actual_rank < per30):
                return "#90D27F"
            elif (actual_rank < per70):
                return "#FFAD71"
            else:
                return "#FF8080"
        
        canvas.create_text(405.0, 300.0, anchor="nw",text=esg_score, fill=what_color(),
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(595.0,300.0,anchor="nw",text=env_score,fill="#192159",
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(780.0,300.0,anchor="nw",text=social_score,fill="#192159",
                           font=("Raleway SemiBold", 48 * -1))
        canvas.create_text(965.0, 300.0,anchor="nw", text=gov_score, fill="#192159",
                           font=("Raleway SemiBold", 48 * -1))

    

def show_company_profile(input_company):
    canvas.create_rectangle(0.0,150.0,295.0,800.0,
                            fill="#F4F4FC",outline="")
    canvas.create_text(122.0,175.0,anchor="nw",text=input_company.upper(),
                       fill="#192159",font=("Raleway SemiBold", 24 * -1))
    logo_list = logo.get_logo(input_company)
    found = False
    for x in logo_list:
        try:
            URL = Request(x, headers={'User-Agent': 'Mozilla/5.0'})
            raw_data = urlopen(URL).read()
            im = Image.open(BytesIO(raw_data))
            photo = ImageTk.PhotoImage(im)
            h = photo.height()
            w = photo.width()
            ratio = min(200/w, 100/h)
            resized = im.resize((int(w*ratio),int(h*ratio)), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized)
            label = tk.Label(image=photo)
            label.image = photo
            label.place(x=50, y = 240)
        except:
            continue
        else:
            found = True
            break
        
    if not found:    
        canvas.create_rectangle(90.0,220.0,204.0,334.0,
                                fill="#AE99C0",outline="")
    canvas.create_text(97.0, 378.0,anchor="nw",text="Continent: Asia",
                       fill="#000000",font=("Raleway Regular", 14 * -1))
    canvas.create_text(98.0,354.0,anchor="nw",text="Country: Singapore",
                       fill="#000000",font=("Raleway Regular", 14 * -1))

def show_summary(input_company):
    result = topic_model.get_summary(input_company)
    if not result:
        result = summary.get_summary(input_company)
    canvas.create_rectangle(359.0,123.0, 1371.0, 290.0, fill="white",outline="")
    canvas.create_text(359.0, 123.0, anchor="nw",text="ESG Article Summarization",fill="#192159",
                       font=("Raleway Bold", 16 * -1))
    sum_label = tk.Label(canvas, text=result, font=("Raleway Bold", 14 * -1),
                 wraplength=900, justify="left", fg="#000000")
    sum_label.place(x=355, y=143)

def show_keywords(input_company):
    canvas.create_text(359.0,440.0,anchor="nw",text="Sustainability Report Topic Modelling",
                       fill="#192159",font=("Raleway Bold", 18 * -1))

def show_membership(input_company):
    canvas.create_rectangle(805.0,480.0,1227.0,602.0,
                            fill="#F4F4FC",outline="")
    canvas.create_rectangle(846.0,480.0,846.0,710.0,
                            fill="#FFFFFF",outline="")
    canvas.create_rectangle(1096.0,480.0,1096.0,710.0,
                            fill="#FFFFFF",outline="")
    canvas.create_rectangle(805.0,480.0,1227.0,710.0,
                            fill="#F5F4FD",outline="")
    canvas.create_text(805.0,440.0,anchor="nw",text="Membership Table",
                       fill="#192159",font=("Raleway Bold", 18 * -1))
    canvas.create_text(816.0,480.0,anchor="nw",text="No.",
                       fill="#AE99C0",font=("Raleway SemiBold", 12 * -1))
    canvas.create_text(867.0,480.0,anchor="nw",text="Membership Name",
                       fill="#AE99C0",font=("Raleway SemiBold", 12 * -1))
    canvas.create_text(1111.0,480.0,anchor="nw",text="Status",
                       fill="#AE99C0",font=("Raleway SemiBold", 12 * -1))

    get_unpri(input_company)
    get_unep_fi(input_company)
    get_icma(input_company)
    get_ungc(input_company)
    get_iigcc(input_company)

def get_unpri(input_company):
    canvas.create_text(822.0,517.0,anchor="nw",text="1",fill="#000000",
                       font=("Raleway Regular", 14 * -1))
    canvas.create_text(867.0,519.0,anchor="nw",text="UNPRI",fill="#000000", font=("Raleway Regular", 12 * -1))
    if (unpri.is_member(input_company) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=510)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=510)

def get_unep_fi(input_company):
    canvas.create_text(822.0,545.0,anchor="nw",text="2",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,548.0,anchor="nw",text="UNEP FI",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (unep_fi.is_member_unepfi(input_company) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=540)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=540)

def get_icma(input_company):
    canvas.create_text(822.0,578.0,anchor="nw",text="3",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,580.0,anchor="nw",text="ICMA",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (icma.is_member_icma(input_company) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=570)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=570)

def get_iigcc(input_company):
    canvas.create_text(822.0,607.0,anchor="nw",text="4",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,609.0,anchor="nw",text="IIGCC",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (iigcc.is_member_iigcc(input_company) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=600)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=600)

def get_ungc(input_company):
    canvas.create_text(822.0,638.0,anchor="nw",text="5",fill="#000000",
                       font=("Raleway Regular", 14 * -1))

    canvas.create_text(867.0,640.0,anchor="nw",text="UNGC",fill="#000000",
                       font=("Raleway Regular", 12 * -1))

    if (ungc.is_member_ungc(input_company) is True):
        logo = Image.open("image_8.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=630)
    else:
        logo = Image.open("image_9.png")
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo, bg="#F5F4FD")
        logo_label.image = logo
        logo_label.place(x=1100, y=630)

def show_topic_model(input_company):
    canvas.create_rectangle(359.0,480.0,760.0,710.0,fill="#F4F4FC",outline="")
    topic_dist = topic_model.get_topic_model(input_company)
    canvas.create_text(532.0, 714.0,anchor="nw",text="Topics",
                       fill="#000000",font=("Raleway Bold", 14 * -1))
    canvas.create_text(332.0,620.0,anchor="nw",text="Proportion",
                       fill="#000000",font=("Raleway Bold", 14 * -1), angle=90)
    data = list(map(lambda x:x[1],topic_dist))

    canvas.create_rectangle(388.0,700.0,740.0,702.0,fill="black",outline="") #Horizontal
    
    canvas.create_rectangle(388.0,500.0,390.0,700.0,fill="black",outline="") #Vertical
    
##    label = list(map(lambda x:"Topic " + str(x[0]),topic_dist))

    canvas.pack()

    c_width = 600
    c_height = 600

    # the variables below size the bar graph
    # experiment with them to fit your needs
    # highest y = max_data_value * y_stretch
    y_stretch = 200
    
    # gap between lower canvas edge and x axis
    y_gap = 30
    
    # stretch enough to get all data items in
    x_stretch = 50
    x_width = 30
    
    # gap between left canvas edge and y axis
    x_gap = 30

    # x place
    x_place = 370
    y_place = 130

    for x, y in enumerate(data):
        # calculate reactangle coordinates (integers) for each bar
        x0 = x_place+ x * x_stretch + x * x_width + x_gap
        y0 = y_place + c_height - (y * y_stretch + y_gap)
        x1 = x_place + x * x_stretch + x * x_width + x_width + x_gap
        y1 = y_place + c_height - y_gap
        # draw the bar
        canvas.create_rectangle(x0, y0, x1, y1, fill="#401564")
        # put the y value above each bar
        canvas.create_text(x0+5, y0, anchor=tk.SW, text=str(round(y,3)))

    
def click():
    label = tk.Label(window, text="Waiting for task to finish.")
    label.pack()

    def task():
        # The window will stay open until this function call ends.
          
        company_name = variable.get().lower()
        show_company_profile(company_name) # Company Profile
        show_summary(company_name) # Summary    
        show_keywords(company_name) #Keywords
        show_membership(company_name) #Membership
        show_esg_rating(company_name) #Ratings
        show_topic_model(company_name)

        #image_image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
        #image_10 = canvas.create_image(515.0,675.0,image=image_image_10)
        root.destroy()
        
    window.after(200, task)
    label.after(1000 , lambda: label.destroy())

#Header Left 
canvas = Canvas(window,bg = "#FFFFFF",height = 814,width = 1371,
                bd = 0,highlightthickness = 0,relief = "ridge")
canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0,0.0,295.0,900.0,fill="#F4F4FC",outline="")

sum_label = tk.Label(canvas, text="", font=("Raleway Bold", 14 * -1),
                     fg="#000000")
sum_label.place(x=355, y=153)

#info Color
image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(438.0,400.0,image=image_image_5)
image_image_6 = PhotoImage(file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(631.0,400.0,image=image_image_6)
image_image_7 = PhotoImage(file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(818.0,400.0,image=image_image_7)

#Right - Title

canvas.create_text(359.0,45.0,anchor="nw",
                   text="Companies’ ESG Performance",fill="#192159",
                   font=("Raleway Bold", 36 * -1))

canvas.create_text(359.0,91.0,anchor="nw",
                   text="Performance based on Ratings,  ESG Keywords, and Membership",
                   fill="#BCBCBC",font=("Raleway Bold", 14 * -1))

#Left - Title

canvas.create_text(102.0,42.0,anchor="nw",text="NatWest Markets",
                   fill="#192159",font=("Raleway Bold", 18 * -1))
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(51.0,52.0,image=image_image_1)

#Search Bar
variable = tk.StringVar(window)

entry_1 = Entry(bd=0,bg="#FFFFFF",textvariable=variable,
                highlightthickness=0)
entry_1.place(x=24.0,y=106.0,width=257.73095703125,
              height=36.19720458984375)
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1,borderwidth=0,
                  highlightthickness=0,command=click,relief="flat")
button_1.place(x=245.0,y=112.0,width=28.0,height=28.0)

window.resizable(False, False)
window.mainloop()
