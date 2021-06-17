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
from random import randint
from station import Station
from databank import Databank
# import asyncio # for reading/writing files without blocking the GUI event loop, may not work?

BODY_COLOUR = "#b4f2ae"
HEADER_COLOUR = "#13db00"


# create root and configure body and header section sizes
root = Tk()
root.columnconfigure(0, weight=100)
header_height = 15
root.rowconfigure(0, weight=header_height) #header
root.rowconfigure(1, weight=100-header_height) #body

# create frame for header
s = ttk.Style()
s.configure("header.TFrame", background=HEADER_COLOUR)
headerFrame = ttk.Frame(root, style="header.TFrame", cursor="none")
headerFrame.grid(column = 0, row = 0, stick=(N, E, S, W))
headerFrame.rowconfigure(0, weight=1)
headerFrame.columnconfigure(0, weight=1)
ttk.Button(headerFrame, text="exit", command=root.destroy).grid(row=0, column=0, sticky=(N, E, S)) # temp button

# create frame for body
s.configure("body.TFrame", background=BODY_COLOUR)
s.configure("body.TLabel", background=BODY_COLOUR)
bodyFrame = ttk.Frame(root, style="body.TFrame", cursor="none")
bodyFrame.grid(column = 0, row = 1, stick=(N, E, S, W))
bodyFrame.rowconfigure(0, weight=1)
bodyFrame.columnconfigure(0, weight=1)


# random styles
n = 3
for r in range(n):
    for g in range(n):
        for b in range(n):
            name = str(r + n*b + n*n*g) + ".TLabel"
            inc = 255//(n-1)
            colour = "#" + f'{inc*r:0>2X}'  + f'{inc*g:0>2X}'  + f'{inc*b:0>2X}' 
            # print(name + " - " + colour)
            s.configure(name, background=colour)
            

# create dashboard
dashboard = Dashboard(bodyFrame)

# connect to station
station = Station()

# load data bank
databank = Databank("/data")

#schedule event for getting new data
def log_data():
    # get current data
    data = station.get_data()
    # record data
    databank.record(data)
    # get data in format for dashboard
    ddata = databank.get_dashboard()
    # set the dashboard data
    dashboard.set_data(ddata)
    root.after(1000, log_data)
log_data()


root.attributes('-fullscreen',True)
root.mainloop()





