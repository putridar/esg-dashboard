import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

import requests
import refinitiv

## DEFINE THE WINDOW

root = tk.Tk()
root.title("ESG Dashboard")



## DEFINE CANVAS

canvas = tk.Canvas(root, width = 1200, height = 900)
canvas.grid(columnspan = 6, rowspan = 6)

## DEFINE HEADER WITH FRAME

header = tk.Frame(root, width = 1200, height = 70, bg="#401564")
header.grid(columnspan = 6, rowspan = 1, row = 0)

## PUT IN THE LOGO IN HEADER

logo = Image.open('natwest-logo.png')
logo = logo.resize((int(logo.size[0]/4),int(logo.size[1]/4)))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo, bg = "#401564")
logo_label.image = logo
logo_label.grid(column=0, row=0, pady=2)

## PUT TITLE IN HEADER

tk.Label(root, text='Companies\' ESG Performance', font='Montserrat 25', bg='#401564', fg='white').\
               grid(column=5, row=0, pady=2)

## COMPANY SEARCH BAR

search_bar = tk.Frame(root, width = 1200, height = 70, bg="red")
search_bar.grid(columnspan = 6, rowspan = 1, row = 1)

instruction = tk.Label(root,
                       text="Company Name",
                       font="Raleway")
instruction.grid(column=0, row=1)

search_btn = Button(root, text="search",
                     #command=lambda:search(),
                     font="shanti")
search_btn.grid(column=2, row=1)

#CODE DUMP

##x = tk.Frame(root, width = 1200, height = 150, bg="pink")
##x.grid(columnspan = 6, row = 1)

search_bar = tk.Frame(root, width = 1200, height = 70, bg="yellow")
search_bar.grid(columnspan = 6, rowspan = 1, row = 2)

x = tk.Frame(root, width = 1200, height = 150, bg="green")
x.grid(columnspan = 6, row = 3)

x = tk.Frame(root, width = 1200, height = 150, bg="yellow")
x.grid(columnspan = 6, row = 4)

x = tk.Frame(root, width = 1200, height = 150, bg="blue")
x.grid(columnspan = 6, row = 5)



root.mainloop()


