from random import randint

class Station:

    def get_data(self):
        directions = ["N", "E", "S", "W", "NE", "SE", "NW", "SW"]
        data = {"temp": randint(5, 40),
                "humidity": randint(0, 100),
                "wind_speed": randint(0, 20),
                "gust_speed": randint(0, 40),
                "wind_direction": directions[randint(0, 7)],
                "rainfall": randint(0, 5)}
        return data