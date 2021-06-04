from tkinter import *
from tkinter import ttk # for GUI
from PIL import ImageTk, Image

class Dashboard:
    
    # constants
    icon_paths = "icons/dashboard/"
    image_bank = []
    
    # temp cell
    current_temp = 0
    min_temp = 0
    max_temp = 0
    # humidity cell
    current_humidity = 0
    min_humidity = 0
    max_humidity = 0
    # wind cell
    wind_speed = 0
    gust_speed = 0
    wind_direction = "N"
    # rain cell
    day_rainfall = 0
    night_rainfall = 0
    
    
    # create dashboard and fill with inital values 
    def __init__(self, parent):
        # main frame for grid, all cells equal size
        mainFrame = ttk.Frame(parent, style="1.TFrame")
        mainFrame.grid(row=0, column=0, stick=(N, E, S, W))
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.columnconfigure(1, weight=1)
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        # frame for each icon
        
        rel_icon_width = 1 #size of icon vs text
        rel_text_width = 1
        
        
        tempFrame = ttk.Frame(mainFrame, style="2.TFrame")
        tempFrame.grid(row=0, column=0, stick=(N, E, S, W))
        tempFrame.columnconfigure(0, weight=rel_icon_width)
        tempFrame.columnconfigure(1, weight=rel_text_width)
        tempFrame.rowconfigure(0, weight=1)
        
        i = Image.open(self.icon_paths + "wind.png")
        i = i.resize((100, 100), Image.ANTIALIAS)
        i = ImageTk.PhotoImage(i)
        self.image_bank.append(i)
        b = ttk.Label(tempFrame, image=self.image_bank[-1])
        b.grid(row = 0, column = 0, sticky=(N, S, E, W))

        
        humidityFrame = ttk.Frame(mainFrame, style="3.TFrame")
        humidityFrame.grid(row=0, column=1, stick=(N, E, S, W))
        humidityFrame.columnconfigure(0, weight=rel_icon_width)
        humidityFrame.columnconfigure(1, weight=rel_text_width)
        humidityFrame.rowconfigure(0, weight=1)
        
        windFrame = ttk.Frame(mainFrame, style="4.TFrame")
        windFrame.grid(row=1, column=0, stick=(N, E, S, W))
        windFrame.columnconfigure(0, weight=rel_icon_width)
        windFrame.columnconfigure(1, weight=rel_text_width)
        windFrame.rowconfigure(0, weight=1)
        
        rainFrame = ttk.Frame(mainFrame, style="5.TFrame")
        rainFrame.grid(row=1, column=1, stick=(N, E, S, W))
        rainFrame.columnconfigure(0, weight=rel_icon_width)
        rainFrame.columnconfigure(1, weight=rel_text_width)
        rainFrame.rowconfigure(0, weight=1)
        
    # Set values for the various data points. All unset data points remain unchanged.
    def set_data(self,
                  new_current_temp=current_temp,
                  new_min_temp=min_temp,
                  new_max_temp=max_temp,
                  new_current_humidity=current_humidity,
                  new_min_humidity=min_humidity,
                  new_max_humidity=max_humidity,
                  new_wind_speed=wind_speed,
                  new_gust_speed=gust_speed,
                  new_wind_direction=wind_direction,
                  new_day_rainfall=day_rainfall,
                  new_night_rainfall=night_rainfall): 
        
        self.current_temp = new_current_temp
        self.min_temp = new_min_temp
        self.max_temp = new_max_temp
        self.current_humidity = new_current_humidity
        self.min_humidity = new_min_humidity
        self.max_humidity = new_max_humidity
        self.wind_speed = new_wind_speed
        self.gust_speed = new_gust_speed
        self.wind_direction = new_wind_direction
        self.day_rainfall = new_day_rainfall
        self.night_rainfall = new_night_rainfall
        
    def update(self):
        pass
    
    
