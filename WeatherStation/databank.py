
class Databank:
    
    short_term = list()
    med_term = list()
    running_aggregates = {"max_temp": None,
                         "min_temp": None,
                         "min_humidity": None,
                         "max_humidity": None,
                         "wind_speed": None,
                         "gust_speed": None,
                         "day_rainfall": None,
                         "night_rainfall": None}
    
    def __init__(self, path=""):
        pass
    
    def record(self, data, datetime):
        self.short_term.append({"datetime": datetime,
                                "data": data})
    
    def get_dashboard(self):
        pass