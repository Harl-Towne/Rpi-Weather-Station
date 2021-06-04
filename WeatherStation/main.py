# raw data
## temperature
## humidity
## wind speed
## wind direction
## rainfall

# data screens
## current data (dashboard)
## graphs
### temperature (min + max + average)
### humidity
### wind speed (avg + gust)
### rainfall
### radial/average wind direction ??

from tkinter import *
from tkinter import ttk # for GUI
from dashboard import Dashboard
from PIL import ImageTk, Image

# import asyncio # for reading/writing files without blocking the GUI event loop, may not work?

# create root and configure body and header section sizes
root = Tk()
root.columnconfigure(0, weight=100)
header_height = 5
root.rowconfigure(0, weight=header_height) #header
root.rowconfigure(1, weight=100-header_height) #body

# create frame for header
s = ttk.Style()
s.configure("header.TFrame", background="dark red")
headerFrame = ttk.Frame(root, style="header.TFrame")
headerFrame.grid(column = 0, row = 0, stick=(N, E, S, W))
headerFrame.rowconfigure(0, weight=1)
headerFrame.columnconfigure(0, weight=1)
ttk.Button(headerFrame, text="exit", command=root.destroy).grid(row=0, column=0) # temp button

# create frame for body
s.configure("body.TFrame", background="dark blue")
bodyFrame = ttk.Frame(root, style="body.TFrame")
bodyFrame.grid(column = 0, row = 1, stick=(N, E, S, W))
bodyFrame.rowconfigure(0, weight=1)
bodyFrame.columnconfigure(0, weight=1)


# random styles
n = 3
for r in range(n):
    for g in range(n):
        for b in range(n):
            name = str(r + 3*b + 9*g) + ".TFrame"
            inc = 255//(n-1)
            colour = "#" + f'{inc*r:0>2X}'  + f'{inc*g:0>2X}'  + f'{inc*b:0>2X}' 
            # print(colour)
            s.configure(name, background=colour)



Dashboard(bodyFrame)
root.attributes('-fullscreen',True)
root.mainloop()





