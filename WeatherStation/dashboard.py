from tkinter import *
from tkinter import ttk # for GUI
from PIL import ImageTk, Image

class Dashboard:
    
    # constants
    icon_path = "icons/dashboard/"
    icons = ["temp.png", "humidity.png", "wind.png", "rain.png"]
    image_bank = []
    
    # text variable for labels
    labelVars = {}
    
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
        # main frame for grid        
        mainFrame = ttk.Frame(parent, style="body.TFrame")
        mainFrame.grid(row=0, column=0, stick=(N, E, S, W))
        
        #configure cell sizes
        rel_icon_width = 1 #size of icon vs text
        rel_text_width = 1
        # mainFrame.columnconfigure(0, weight=rel_icon_width)
        mainFrame.columnconfigure(1, weight=rel_text_width)
        # mainFrame.columnconfigure(2, weight=rel_icon_width)
        mainFrame.columnconfigure(3, weight=rel_text_width)
        mainFrame.rowconfigure(0, weight=1)
        mainFrame.rowconfigure(1, weight=1)
        
        # place icons
        for i, icon in enumerate(self.icons):
            # get image
            img = Image.open(self.icon_path + icon)
            img = img.resize((180, 180), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            
            #save image
            self.image_bank.append(img)
            
            # put image in label
            c = (i*2)%4
            r = i//2
            imgCon = ttk.Label(mainFrame, image=self.image_bank[-1], style="body.TLabel")
            imgCon.grid(row = r, column = c, sticky=(N, S, E, W))
            
        # initialise all variables for text labels
        self.labelVars = {"current_temp": StringVar(),
                         "max_temp": StringVar(),
                         "min_temp": StringVar(),
                         "current_humidity": StringVar(),
                         "min_humidity": StringVar(),
                         "max_humidity": StringVar(),
                         "wind_speed": StringVar(),
                         "gust_speed": StringVar(),
                         "wind_direction": StringVar(),
                         "day_rainfall": StringVar(),
                         "night_rainfall": StringVar()}
        
        # create all labels and place them on the screen            
        tempFrame = ttk.Frame(mainFrame)
        tempFrame.grid(row=0, column=1)
        ttk.Label(tempFrame, textvariable=self.labelVars['current_temp']).grid(row=0, column=0)
        ttk.Label(tempFrame, textvariable=self.labelVars['max_temp']).grid(row=1, column=0)
        ttk.Label(tempFrame, textvariable=self.labelVars['min_temp']).grid(row=2, column=0)
        
        humidityFrame = ttk.Frame(mainFrame)
        humidityFrame.grid(row=0, column=3)
        ttk.Label(humidityFrame, textvariable=self.labelVars['current_humidity']).grid(row=0, column=0)
        ttk.Label(humidityFrame, textvariable=self.labelVars['max_humidity']).grid(row=1, column=0)
        ttk.Label(humidityFrame, textvariable=self.labelVars['min_humidity']).grid(row=2, column=0)
        
        windFrame = ttk.Frame(mainFrame)
        windFrame.grid(row=1, column=1)
        ttk.Label(windFrame, textvariable=self.labelVars['wind_speed']).grid(row=0, column=0)
        ttk.Label(windFrame, textvariable=self.labelVars['gust_speed']).grid(row=1, column=0)
        ttk.Label(windFrame, textvariable=self.labelVars['wind_direction']).grid(row=2, column=0)
        
        rainFrame = ttk.Frame(mainFrame)
        rainFrame.grid(row=1, column=3)
        ttk.Label(rainFrame, textvariable=self.labelVars['day_rainfall']).grid(row=0, column=0)
        ttk.Label(rainFrame, textvariable=self.labelVars['night_rainfall']).grid(row=1, column=0)
        
        # put correct text in labels
        self.set_data()
        
    # Set values for the various data points. All unset data points remain unchanged.
    def set_data(self, data): 
        
        # update varaibles
        self.current_temp = data["current_temp"]
        self.min_temp = data["min_temp"]
        self.max_temp = data["max_temp"]
        self.current_humidity = data["current_humidity"]
        self.min_humidity = data["min_humidity"]
        self.max_humidity = data["max_humidity"]
        self.wind_speed = data["wind_speed"]
        self.gust_speed = data["gust_speed"]
        self.wind_direction = data["wind_direction"]
        self.day_rainfall = data["day_rainfall"]
        self.night_rainfall = data["night_rainfall"]
        
        # update text in labels
        self.update()
        
    def update(self):
        # update text for all labels
        self.labelVars['current_temp'].set(str(self.current_temp) + "\N{DEGREE SIGN}")
        self.labelVars['max_temp'].set("Max: " + str(self.max_temp) + "\N{DEGREE SIGN}")
        self.labelVars['min_temp'].set("Min: " + str(self.min_temp) + "\N{DEGREE SIGN}")

        self.labelVars['current_humidity'].set(str(self.current_humidity) + "%")
        self.labelVars['max_humidity'].set("Max: " + str(self.max_humidity) + "%")
        self.labelVars['min_humidity'].set("Min: " + str(self.min_humidity) + "%")
        
        self.labelVars['wind_speed'].set(str(self.wind_speed) + "Km/h")
        self.labelVars['gust_speed'].set("Gust: " + str(self.gust_speed) + "Km/h")
        self.labelVars['wind_direction'].set(self.wind_direction)
        
        self.labelVars['day_rainfall'].set("Day: " + str(self.day_rainfall) + "mm")
        self.labelVars['night_rainfall'].set("Night: " + str(self.night_rainfall) + "mm")
    
    
